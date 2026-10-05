from django.conf import settings
from django.contrib import messages
from django.db.models import Count, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from . import share
from .models import Check, Entry, Enquiry, ListType, Place, Report
from .visibility import entry_view, name_only


def resolve_place(path):
    node = Place.objects.filter(kind="world", parent=None).first()
    if node is None:
        raise Http404
    for slug in [s for s in path.split("/") if s]:
        node = get_object_or_404(Place, parent=node, slug=slug)
    return node


def place_url(place):
    return "/p/" + place.path if place.path else "/"


def entries_under(place):
    return Entry.objects.filter(place_id__in=place.descendant_ids()).select_related("place")


def trust(entries):
    total = entries.count()
    if not total:
        return {"total": 0, "s": 0, "o": 0, "a": 0, "pct": 0}
    lv = {Check.Level.SURVEYOR: 0, Check.Level.OWNER: 0, Check.Level.AI: 0}
    for e in entries.prefetch_related("checks"):
        b = e.best_level()
        if b in lv:
            lv[b] += 1
    s, o, a = (round(100 * lv[k] / total) for k in (Check.Level.SURVEYOR, Check.Level.OWNER, Check.Level.AI))
    return {"total": total, "s": s, "o": o, "a": a, "pct": s + o}


def crumbs(place):
    return [{"label": p.name, "label_ur": p.name_ur, "href": place_url(p)} for p in place.ancestors()]


def is_own_place(request, place):
    mp = request.my_place
    return bool(mp and (place.pk in mp.descendant_ids()))


def home(request):
    world = Place.objects.filter(kind="world", parent=None).first()
    countries = world.children.filter(kind="country") if world else Place.objects.none()
    near = None
    if request.my_place:
        near = {"place": request.my_place, "url": place_url(request.my_place),
                "count": entries_under(request.my_place).count()}
    return render(request, "lists/home.html", {"countries": countries, "near": near,
                                                "all_places": Place.objects.exclude(kind="world").order_by("name")[:300]})


def place_page(request, path):
    place = resolve_place(path)
    children = list(place.children.all())
    types = (ListType.objects.filter(entries__place_id__in=place.descendant_ids())
             .annotate(n=Count("entries", filter=Q(entries__place_id__in=place.descendant_ids()), distinct=True))
             .order_by("name"))
    return render(request, "lists/place.html", {
        "place": place, "children": [{"p": c, "url": place_url(c), "n": entries_under(c).count()} for c in children],
        "types": types, "crumbs": crumbs(place), "place_url": place_url(place),
        "total": entries_under(place).count()})


def list_page(request, path, type_slug):
    place = resolve_place(path)
    ltype = get_object_or_404(ListType, slug=type_slug)
    qs = entries_under(place).filter(list_types=ltype).prefetch_related("checks", "socials", "services", "identifiers")
    tr = trust(qs)
    areas = list(Place.objects.filter(pk__in=qs.values_list("place_id", flat=True)).order_by("name"))
    area = request.GET.get("area", "")
    q = request.GET.get("q", "").strip()[:100]
    sort = request.GET.get("sort", "name")
    if area:
        qs = qs.filter(place__slug=area)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(name_alt__icontains=q) | Q(entry_type__icontains=q))
    if sort == "checked":
        qs = sorted(qs, key=lambda e: e.last_checked() or e.created_at.date(), reverse=True)
    else:
        qs = list(qs.order_by("-sponsored", "name"))
    own = is_own_place(request, place)
    names_only = not (request.subscriber or own)
    total = len(qs)
    if names_only:
        rows = [name_only(e) for e in qs[:settings.FREE_PREVIEW_NAMES]]
    else:
        rows = [entry_view(e, request.subscriber) for e in qs]
    for r in rows:
        r["url"] = f"/e/{r['entry'].pk}/"
    url = request.build_absolute_uri(request.path)
    return render(request, "lists/list.html", {
        "place": place, "ltype": ltype, "rows": rows, "total": total, "shown": len(rows), "trust": tr,
        "areas": areas, "area": area, "q": q, "sort": sort, "names_only": names_only,
        "crumbs": crumbs(place), "own": own,
        "share_links": share.build(f"{ltype.name} in {place.name}", f"{total} listed.", url, "list_share")})


def entry_page(request, pk):
    e = get_object_or_404(Entry.objects.select_related("place"), pk=pk)
    d = entry_view(e, request.subscriber)
    d["checks"] = list(e.checks.all())
    ltype = e.list_types.first()
    url = request.build_absolute_uri(request.path)
    return render(request, "lists/entry.html", {
        "e": d, "entry": e, "crumbs": crumbs(e.place), "ltype": ltype,
        "share_links": share.build(f"{e.name}, {e.entry_type}, {e.place.name}",
                                   f"Last checked {d['last_checked']}." if d["last_checked"] else "Listed on AllLists.",
                                   url, "entry_share")})


@require_POST
def enquiry(request):
    if not request.subscriber:
        messages.error(request, "subscribers_only")
        return redirect(request.POST.get("next") or "/")
    ids = [int(i) for i in request.POST.getlist("entries") if i.isdigit()][:50]
    msg = request.POST.get("message", "").strip()[:2000]
    mail = request.POST.get("reply_to", "").strip()[:200]
    entries = Entry.objects.filter(pk__in=ids)
    if not (entries and msg and "@" in mail):
        return HttpResponse("Bad request", status=400)
    enq = Enquiry.objects.create(sender=request.user if request.user.is_authenticated else None,
                                 reply_to=mail, message=msg)
    enq.entries.set(entries)
    messages.success(request, "enquiry_sent")
    return redirect(safe_next(request, "/"))


@require_POST
def report(request, pk, kind):
    if kind not in ("report", "claim"):
        raise Http404
    e = get_object_or_404(Entry, pk=pk)
    Report.objects.create(entry=e, kind=kind, note=request.POST.get("note", "")[:1000],
                          contact=request.POST.get("contact", "")[:200])
    messages.success(request, "submitted")
    return redirect(f"/e/{e.pk}/")


def safe_next(request, default="/"):
    nxt = request.POST.get("next", "")
    ok = url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure())
    return nxt if nxt and ok else default


@require_POST
def prefs(request):
    resp = redirect(safe_next(request))
    for key, allowed in (("lang", ("en", "ur")), ("theme", ("light", "dark", "")), ("view", ("list", "cards"))):
        v = request.POST.get(key)
        if v is not None and v in allowed:
            resp.set_cookie(key, v, max_age=60 * 60 * 24 * 365, samesite="Lax", httponly=False)
    plan = request.POST.get("plan")
    if settings.DEMO_MODE and plan in ("free", "subscriber"):
        request.session["demo_plan"] = plan
    pid = request.POST.get("place")
    if pid and pid.isdigit() and Place.objects.filter(pk=pid).exists():
        request.session["place_id"] = int(pid)
    return resp


def healthz(request):
    return HttpResponse("ok", content_type="text/plain")


def not_found(request, exception=None):
    return render(request, "lists/404.html", status=404)
