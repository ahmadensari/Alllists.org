"""Public views. Shell views never read the session or cookies, so one address gives everyone the same bytes (R05).
Personal parts (plan, location, ads, details) are served as private fragments under /_f/."""

import hashlib

from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.cache import get_conditional_response
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_POST

from access import placements, quotas
from access import services as access_services
from access.policy import Viewer, list_mode, subscribes_to, visible
from analytics.models import RollupCell
from core.models import CountrySwitch
from entries.models import Entry
from places.models import Place
from taxonomy.models import ListTypeSettings

from . import maps, search
from . import format as fmt
from entries import services as es

from . import queries, resolver, seo, share, strings
from .location import viewer_place
from .resolver import list_url, place_url

CHECK_ORDER = {"surveyor": 0, "owner": 1, "ai": 2, "none": 3}


# ---- helpers -------------------------------------------------------------------------------------------------


def shell(request, template, ctx, stamp):
    """Render a shared page with an ETag from template version, language, path, query and data stamp."""
    raw = "|".join(
        [settings.TEMPLATE_VERSION, request.lang, request.path_info, request.META.get("QUERY_STRING", ""), stamp]
    )
    etag = '"' + hashlib.sha256(raw.encode()).hexdigest()[:24] + '"'
    cond = get_conditional_response(request, etag=etag)
    if cond is not None:
        cond["ETag"] = etag
        return cond
    response = render(request, template, ctx)
    response["ETag"] = etag
    response["Cache-Control"] = "public, max-age=0, s-maxage=300, stale-while-revalidate=600"
    return response


def private(response):
    response["Cache-Control"] = "private, no-store"
    response["Vary"] = "Cookie"
    response["X-Robots-Tag"] = "noindex"
    return response


def get_viewer(request):
    """Fragments only. Subscriber access is the demo switch until real subscriptions exist (plan P3.04)."""
    place, source = viewer_place(request)
    sub = settings.DEMO_MODE and request.session.get("demo_plan") == "subscriber"
    scopes = tuple(access_services.active_scopes(request.user))
    return Viewer(subscriber=bool(sub), own_path=place.path if place else None, scopes=scopes), place, source


def breadcrumb(place):
    return [{"place": p, "url": place_url(p)} for p in queries.ancestors_of(place)]


def check_chips(entry, now):
    """Current and past checks for an entry, best first, for display."""
    rows = []
    for v in entry.verification_current.all():
        current = v.state == "verified" and v.expires_at and v.expires_at > now
        rows.append(
            {
                "level": v.level,
                "group": v.field_group,
                "date": v.verified_at,
                "who": v.actor_display,
                "method": v.method,
                "current": bool(current),
                "expired": v.state == "expired" or (v.state == "verified" and not current),
                "revoked": v.state == "revoked",
            }
        )
    return sorted(rows, key=lambda r: (not r["current"], CHECK_ORDER.get(r["level"], 9)))


def row_for(entry, lang, prefix, now):
    level = queries.best_level(entry, now)
    return {
        "uid": entry.uid,
        "name": entry.name,
        "alt": queries.alt_name(entry, lang),
        "level": level,
        "checked": entry.last_verified_at,
        "area": entry.place,
        "type": entry.primary_concept,
        "company": es.company_page_active(entry),
        "status": entry.status,
        "closed": entry.status in ("permanently_closed",),
        "url": f"/e/{entry.uid}/{_slug(entry.name)}/",
    }


def _slug(name):
    from django.utils.text import slugify

    return slugify(name)[:60] or "entry"


COMPANY_KINDS = [
    ("about", "cs_about"),
    ("products", "cs_products"),
    ("capacity", "cs_capacity"),
    ("terms", "cs_terms"),
    ("faq", "cs_faq"),
]


def company_sections(entry):
    """Approved company-provided sections, grouped by kind, only while the paid plan is active."""
    if not (es.company_page_active(entry) and es.company_page_allowed(entry)):
        return {}
    out = {}
    for sec in entry.company_sections.filter(state="approved").order_by("kind", "sort", "id"):
        out.setdefault(sec.kind, []).append(sec)
    return out


def company_updated(entry):
    secs = [s.updated_at for s in entry.company_sections.filter(state="approved")]
    return max(secs) if secs else None


def company_certs(entry):
    """Certificates the company lists: "Checked by AllLists" only when a check was recorded, else "Company says"."""
    if not (es.company_page_active(entry) and es.company_page_allowed(entry)):
        return []
    return [
        {"scheme": i.scheme, "value": i.value, "checked": i.last_checked is not None, "date": i.last_checked}
        for i in entry.identifier_set.all()
    ]


def specialities_of(entry):
    out = [s.concept.label("en") for s in entry.speciality_set.select_related("concept")]
    cats = (entry.addons or {}).get("product_categories") or []
    out += [c for c in cats if isinstance(c, str)]
    return list(dict.fromkeys(out))


# ---- pages ---------------------------------------------------------------------------------------------------


@require_GET
def world(request):
    return place_page(request, resolver.world())


def dispatch(request, path):
    hit = resolver.resolve(path)
    if hit is None:
        raise Http404
    if hit[0] == "place":
        return place_page(request, hit[1])
    return list_page(request, hit[1], hit[2])


def place_page(request, place):
    if place is None:
        raise Http404
    children = queries.child_counts(place)
    here = list(queries.lists_here(place))
    from taxonomy.models import Concept

    concepts = {
        c.pk: c for c in Concept.objects.filter(pk__in=[h["concept_id"] for h in here]).prefetch_related("labels")
    }
    tiles = [
        {"concept": concepts[h["concept_id"]], "n": h["n"], "url": list_url(place, concepts[h["concept_id"]])}
        for h in here
    ]
    total = queries.place_total(place)
    cell_stamp = (
        RollupCell.objects.filter(place_path__startswith=place.path)
        .order_by("-updated_at")
        .values_list("updated_at", flat=True)
        .first()
    )
    path = place_url(place)
    ctx = {
        "place": place,
        "crumbs": breadcrumb(place),
        "children": [(c, n, place_url(c)) for c, n in children if True],
        "tiles": tiles,
        "total": total,
        "is_world": place.level == "world",
        "path": path,
        "title": strings.t(
            request.lang, "title_home" if place.level == "world" else "title_place", place=place.name_for(request.lang)
        ),
        "robots": seo.robots_meta(False),
        "alternates": seo.alternates(request, path),
        "canonical": request.build_absolute_uri(request.prefix + path),
        "fragment": request.prefix + "/_f/near-you/?path=" + place.path,
    }
    return shell(request, "catalog/place.html", ctx, queries.stamp(cell_stamp))


def list_page(request, place, concept):
    lang, now = request.lang, timezone.now()
    cell = queries.rollup(place, concept)
    area_slug = request.GET.get("area", "")
    area_place = Place.objects.filter(parent=place, slug=area_slug, status="active").first() if area_slug else None
    sort = request.GET.get("sort") if request.GET.get("sort") in ("name", "checked") else ""
    qs = queries.list_rows_queryset(place, concept, area_place, sort or "name")
    page = Paginator(qs, settings.PAGE_SIZE).get_page(request.GET.get("page"))
    rows = [row_for(e, lang, request.prefix, now) for e in page]
    sponsored = placements.active_placements(place.path, concept.pk) if not area_slug and page.number == 1 else []
    sponsored_rows = [{**row_for(p.entry, lang, request.prefix, now), "sponsored": True} for p in sponsored]
    chips = queries.area_chips(place, concept)
    last = queries.last_checked(place, concept)
    published, awaiting = cell["published"], max(cell["total"] - cell["published"], 0)
    params = {"area": area_slug if area_place else "", "sort": sort, "page": page.number if page.number > 1 else 0}
    path = list_url(place, concept)
    names = {"list_type": concept.label(lang), "place": place.name_for(lang)}
    cs = ListTypeSettings.objects.filter(concept=concept).first()
    ctx = {
        "scope_path": place.path,
        "place": place,
        "concept": concept,
        "crumbs": breadcrumb(place),
        "rows": rows,
        "sponsored_rows": sponsored_rows,
        "page": page,
        "chips": [(c, n) for c, n in chips],
        "area": area_place,
        "sort": sort,
        "cell": cell,
        "trust": queries.trust_split(cell),
        "published": published,
        "awaiting": awaiting,
        "last": last,
        "empty": published == 0,
        "path": path,
        "params": params,
        "names": names,
        "title": strings.t(lang, "title_list", **names),
        "robots": seo.robots_meta(seo.indexable_list(place, concept, cell, request.GET)),
        "canonical": request.build_absolute_uri(request.prefix + path),
        "alternates": seo.alternates(request, path),
        "share_links": share.build(
            strings.t(lang, "list_title", **names),
            strings.t(lang, "n_published", n=published),
            request.build_absolute_uri(request.prefix + path),
            "list_share",
            hidden=bool(cs and cs.share_hidden),
        ),
        "jsonld": seo.list_jsonld(
            lang, strings.t(lang, "list_title", **names), request.build_absolute_uri(request.prefix + path), rows
        ),
        "fragment": request.prefix
        + "/_f/list/?"
        + "&".join(
            f"{k}={v}"
            for k, v in {"path": place.path, "type": concept.slug, **{k: v for k, v in params.items() if v}}.items()
        ),
    }
    stamp = (
        queries.stamp(cell["updated_at"], last)
        + "|"
        + ",".join(f"{p.pk}.{int(p.updated_at.timestamp())}" for p in sponsored)
    )
    return shell(request, "catalog/list.html", ctx, stamp)


def entry_page(request, uid, slug=None):
    lang, now = request.lang, timezone.now()
    entry = (
        Entry.objects.select_related("place", "primary_concept")
        .prefetch_related("verification_current", "namevariant_set", "speciality_set")
        .filter(uid=uid, deleted_at__isnull=True)
        .first()
    )
    if entry is None or entry.merged_into_id and entry.merged_into is None:
        raise Http404
    if entry.merged_into_id:
        return redirect(request.prefix + f"/e/{entry.merged_into.uid}/{_slug(entry.merged_into.name)}/", permanent=True)
    if entry.publish_state != Entry.PublishState.PUBLISHED:
        raise Http404
    canonical_slug = _slug(entry.name)
    if slug != canonical_slug:
        return redirect(request.prefix + f"/e/{entry.uid}/{canonical_slug}/", permanent=True)
    level = queries.best_level(entry, now)
    checks = check_chips(entry, now)
    addons = entry.addons or {}
    free_details = []
    from taxonomy.models import AddonField

    if entry.primary_concept.template_id:
        for f in AddonField.objects.filter(
            template_id=entry.primary_concept.template_id, deprecated_at__isnull=True
        ).order_by("id"):
            val = addons.get(f.key)
            if f.show == "P" and val not in (None, "", [], {}) and f.type in ("enum", "bool", "number", "text"):
                free_details.append((f.key, val))
    locked_fields = (
        [
            f.key
            for f in AddonField.objects.filter(
                template_id=entry.primary_concept.template_id, show="L", deprecated_at__isnull=True
            )
        ]
        if entry.primary_concept.template_id
        else []
    )
    cs = ListTypeSettings.objects.filter(concept=entry.primary_concept).first()
    hidden_share = bool(
        (cs and cs.share_hidden) or entry.entity_type == "person" or "do_not_share" in (entry.visibility_flags or [])
    )
    path = f"/e/{entry.uid}/{canonical_slug}/"
    url = request.build_absolute_uri(request.prefix + path)
    list_type_name = entry.primary_concept.label(lang)
    place_name = entry.place.name_for(lang)
    last = max([c["date"] for c in checks if c["date"]], default=None)
    ctx = {
        "entry": entry,
        "place": entry.place,
        "concept": entry.primary_concept,
        "alt": queries.alt_name(entry, lang),
        "level": level,
        "checks": checks,
        "last": last,
        "specialities": specialities_of(entry)[:3],
        "more_specialities": max(len(specialities_of(entry)) - 3, 0),
        "free_details": free_details,
        "locked_fields": locked_fields,
        "crumbs": breadcrumb(entry.place),
        "path": path,
        "list_url": list_url(entry.place, entry.primary_concept),
        "closed": entry.status == "permanently_closed",
        "status_label": {
            "temporarily_closed": "temporarily_closed",
            "moved": "moved",
            "permanently_closed": "closed",
        }.get(entry.status),
        "company": es.company_page_active(entry),
        "company_kinds": COMPANY_KINDS,
        "company_sections": company_sections(entry),
        "company_certs": company_certs(entry),
        "company_updated": company_updated(entry),
        "services": [s.name_text for s in entry.service_set.all()],
        "certs": [i.scheme for i in entry.identifier_set.all()],
        "title": strings.t(lang, "title_entry", name=entry.name, list_type=list_type_name, place=place_name),
        "robots": seo.robots_meta(seo.indexable_entry(entry, level)),
        "canonical": url,
        "alternates": seo.alternates(request, path),
        "share_links": share.build(
            f"{entry.name}, {list_type_name}, {place_name}",
            strings.t(lang, "last_checked", date=fmt.fmt_date(lang, last)) if last else "",
            url,
            "entry_share",
            hidden=hidden_share,
        ),
        "jsonld": seo.entry_jsonld(entry, entry.place, url),
        "fragment": f"{request.prefix}/_f/entry/{entry.uid}/",
    }
    return shell(request, "catalog/entry.html", ctx, queries.stamp(entry.updated_at, entry.last_verified_at))


# ---- fragments (private, never cached, never indexed) -----------------------------------------------------------


@require_GET
def frag_near_you(request):
    viewer, place, source = get_viewer(request)
    steps = []
    if place:
        for p in place.ancestors()[::-1]:
            steps.append({"place": p, "url": place_url(p), "n": queries.place_total(p)})
    resp = render(
        request,
        "catalog/fragments/near_you.html",
        {
            "place": place,
            "source": source,
            "steps": steps,
            "demo_plan": "subscriber" if viewer.subscriber else "free",
            "all_places": Place.objects.filter(status="active").exclude(level="world").order_by("path")[:300],
        },
    )
    return private(resp)


@require_GET
def frag_list(request):
    viewer, place, source = get_viewer(request)
    lp = Place.objects.filter(path=request.GET.get("path", ""), status="active").first()
    concept = resolve_concept(request.GET.get("type", ""))
    if lp is None or concept is None:
        return private(HttpResponse("", status=204))
    if not quotas.note_fragment(request):
        return private(HttpResponse("", status=429))
    from analytics import events

    events.emit("list_view", request, path=lp.path, type=concept.slug)
    mode = list_mode(viewer, lp.path, concept.pk)
    area_slug = request.GET.get("area", "")
    area_place = Place.objects.filter(parent=lp, slug=area_slug, status="active").first() if area_slug else None
    sort = request.GET.get("sort") if request.GET.get("sort") in ("name", "checked") else "name"
    qs = queries.list_rows_queryset(lp, concept, area_place, sort)
    page = Paginator(qs, settings.PAGE_SIZE).get_page(request.GET.get("page"))
    quota_exceeded = False
    if mode == "free":
        allowed, remaining, limit = quotas.check_names(request, len(page.object_list))
        if not allowed:
            mode, quota_exceeded = "names", True
    details = []
    for e in page:
        specs = specialities_of(e)
        details.append(
            {
                "uid": e.uid,
                "type": e.primary_concept,
                "specs": specs if mode == "full" else specs[:3],
                "more": 0 if mode == "full" else max(len(specs) - 3, 0),
            }
        )
    resp = render(
        request,
        "catalog/fragments/list_detail.html",
        {
            "mode": mode,
            "details": details,
            "viewer": viewer,
            "ads": visible("ads", viewer, lp.path, concept.pk) != "none",
            "ad": _ad_for(viewer, lp.path, concept.pk),
            "quota_exceeded": quota_exceeded,
            "names_only": mode == "names",
            "locked": mode != "full",
        },
    )
    return private(resp)


@require_GET
def ad_click(request, pk):
    """Count a click on a text ad, then go to the entry page it points to. Never indexed."""
    from access.models import Ad
    from django.db.models import F

    ad = Ad.objects.select_related("entry").filter(pk=pk, state="active").first()
    if ad is None or ad.entry.publish_state != "published":
        raise Http404
    Ad.objects.filter(pk=ad.pk).update(clicks=F("clicks") + 1)
    resp = redirect(f"/e/{ad.entry.uid}/{_slug(ad.entry.name)}/")
    resp["X-Robots-Tag"] = "noindex"
    return resp


def _ad_for(viewer, place_path, concept_id):
    """One text ad for a free viewer in the matching trade and place; subscribers never see ads."""
    if visible("ads", viewer, place_path, concept_id) == "none":
        return None
    ad = placements.pick_ad(place_path, concept_id)
    if ad is not None:
        placements.note_shown(ad)
    return ad


@require_GET
def frag_entry(request, uid):
    viewer, place, source = get_viewer(request)
    entry = (
        Entry.objects.select_related("place", "primary_concept")
        .filter(uid=uid, publish_state="published", deleted_at__isnull=True)
        .first()
    )
    if entry is None:
        return private(HttpResponse("", status=204))
    full = subscribes_to(viewer, entry.place_path, entry.primary_concept_id)
    ctx = {
        "entry": entry,
        "full": full,
        "ads": visible("ads", viewer, entry.place_path, entry.primary_concept_id) != "none",
        "ad": _ad_for(viewer, entry.place_path, entry.primary_concept_id),
        "socials": list(entry.social_set.all()) if full else [],
        "services": list(entry.service_set.all()) if full else [],
        "identifiers": list(entry.identifier_set.all()) if full else [],
        "addons_locked": [],
        "map_links": maps.links(entry.lat, entry.lon, entry.country_code) if full and entry.lat is not None else {},
        "can_message": entry.status != "permanently_closed"
        and visible("enquiry_one", viewer, entry.place_path, entry.primary_concept_id) != "none",
    }
    if full and entry.primary_concept.template_id:
        from taxonomy.models import AddonField

        for f in AddonField.objects.filter(
            template_id=entry.primary_concept.template_id, show="L", deprecated_at__isnull=True
        ):
            val = (entry.addons or {}).get(f.key)
            if val not in (None, "", [], {}):
                ctx["addons_locked"].append((f.key, val))
    return private(render(request, "catalog/fragments/entry_detail.html", ctx))


def resolve_concept(slug):
    from taxonomy.models import Concept

    return Concept.objects.filter(kind="list_type", slug=slug, status="active").first()


# ---- preferences (demo plan and place choice need the session; theme, view and language do not) ---------------------


@require_POST
def prefs_location(request):
    """Exact location from the browser button: matched to the nearest place, kept in the session only, never stored."""
    from .location import nearest_place

    try:
        place = nearest_place(request.POST.get("lat", ""), request.POST.get("lon", ""))
    except ValueError:
        place = None
    if place:
        request.session["place_uid"] = place.uid
    nxt = request.POST.get("next", "/")
    ok = url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure())
    return redirect(nxt if ok else "/")


@require_POST
def prefs(request):
    nxt = request.POST.get("next", "/")
    ok = url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure())
    resp = redirect(nxt if ok else "/")
    plan = request.POST.get("plan")
    if settings.DEMO_MODE and plan in ("free", "subscriber"):
        request.session["demo_plan"] = plan
    uid = request.POST.get("place")
    if uid and Place.objects.filter(uid=uid, status="active").exists():
        request.session["place_uid"] = uid
    return resp


# ---- machine pages ---------------------------------------------------------------------------------------------


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /_f/",
        "Disallow: /admin/",
        "Disallow: /staff/",
        "Disallow: /account/",
        "Disallow: /search/",
        "Disallow: /prefs/",
        "",
        "# Thin pages are marked noindex in the page itself; they are not blocked here so the marker can be read.",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


SITEMAP_SIZE = 50000


def indexable_list_cells(country_code):
    switch = CountrySwitch.for_country(country_code)
    if not switch.indexing_on:
        return []
    out = []
    for c in (
        RollupCell.objects.filter(country_code=country_code, concept__kind="list_type", place_path__gt="")
        .select_related("concept")
        .order_by("place_path", "concept_id")
    ):
        verified = c.by_level.get("surveyor", 0) + c.by_level.get("owner", 0)
        cs = ListTypeSettings.objects.filter(concept=c.concept).first()
        if verified >= (cs.index_threshold if cs else settings.INDEX_THRESHOLD):
            out.append(c)
    return out


@require_GET
def sitemap_index(request):
    parts = []
    for code in sorted(set(RollupCell.objects.values_list("country_code", flat=True))):
        n = len(indexable_list_cells(code))
        for i in range(max(1, -(-n // SITEMAP_SIZE)) if n else 0):
            parts.append(request.build_absolute_uri(f"/sitemaps/{code.lower()}-{i + 1}.xml"))
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    xml += [f"<sitemap><loc>{p}</loc></sitemap>" for p in parts]
    xml.append("</sitemapindex>")
    return HttpResponse("\n".join(xml), content_type="application/xml")


@require_GET
def sitemap_shard(request, cc, n):
    cells = indexable_list_cells(cc.upper())
    chunk = cells[(n - 1) * SITEMAP_SIZE : n * SITEMAP_SIZE]
    if not chunk:
        raise Http404
    places = {p.path: p for p in Place.objects.filter(path__in={c.place_path for c in chunk})}
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for c in chunk:
        p = places.get(c.place_path)
        if p:
            loc = request.build_absolute_uri(list_url(p, c.concept))
            xml.append(f"<url><loc>{loc}</loc><lastmod>{c.updated_at.date().isoformat()}</lastmod></url>")
    xml.append("</urlset>")
    return HttpResponse("\n".join(xml), content_type="application/xml")


@require_GET
def healthz(request):
    return HttpResponse("ok", content_type="text/plain")


def not_found(request, exception=None):
    lang = getattr(request, "lang", "en")
    return render(
        request,
        "catalog/404.html",
        {
            "lang": lang,
            "dir": "rtl" if lang == "ur" else "ltr",
            "prefix": getattr(request, "prefix", ""),
            "title": strings.t(lang, "not_found"),
        },
        status=404,
    )


# ---- search ------------------------------------------------------------------------------------------------------


@require_GET
def search_page(request):
    from analytics import events

    scope = search.scope_from_path(request.GET.get("scope", ""))
    results = search.run(request.GET.get("q", ""), scope)
    lang, now = request.lang, timezone.now()
    entry_rows = [row_for(e, lang, request.prefix, now) for e in results["entries"]]
    concept_links = [(c, list_url(scope or resolver.world(), c)) for c in results["concepts"]]
    place_links = [(p, place_url(p)) for p in results["places"]]
    if results["query"]:
        events.emit("search", request, n=search.total(results), scoped=bool(scope))
        if search.total(results) == 0:
            events.emit("search_zero_result", request)
    if request.GET.get("fragment"):
        return private(render(request, "catalog/search_rows.html", {"rows": entry_rows}))
    resp = render(
        request,
        "catalog/search.html",
        {
            "q": results["query"],
            "scope": scope,
            "concept_links": concept_links,
            "place_links": place_links,
            "rows": entry_rows,
            "none": bool(results["query"]) and search.total(results) == 0,
            "short": 0 < len(results["query"]) < 2,
            "robots": "noindex,follow",
            "title": strings.t(lang, "search_everything"),
            "canonical": "",
        },
    )
    resp["Cache-Control"] = "private, no-store"
    return resp
