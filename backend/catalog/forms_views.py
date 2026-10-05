"""Forms and relay pages (plan 8.3.4, 13, 6.5). Server-rendered, one layout, errors summarised at the top."""

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from access import services as access_services
from access.policy import Viewer, subscribes_to
from accounts import throttle
from accounts.roles import has_cap
from core.models import CountrySwitch
from entries import services as es
from entries.models import Entry
from moderation import services as mod
from outreach import services as relay
from outreach.models import Enquiry
from places.models import Place
from places.services import propose_area
from taxonomy.models import AddonField, Concept
from volunteers.services import ensure_profile

from . import queries

LOGIN = "/account/login/"


def _page(request, template, ctx, status=200):
    ctx.setdefault("robots", "noindex,follow")
    ctx.setdefault("title", "AllLists")
    return render(request, template, ctx, status=status)


def _entry_or_404(uid, published_only=True):
    qs = Entry.objects.select_related("place", "primary_concept").filter(
        uid=uid, deleted_at__isnull=True, merged_into__isnull=True
    )
    qs = (
        qs.filter(publish_state="published")
        if published_only
        else qs.exclude(publish_state__in=["tombstoned", "suppressed"])
    )
    e = qs.first()
    if e is None:
        raise Http404
    return e


def _list_types():
    return list(Concept.objects.filter(kind="list_type", status="active").prefetch_related("labels").order_by("slug"))


def _places():
    return list(Place.objects.filter(status="active").exclude(level="world").order_by("path")[:500])


# ---- add an entry ------------------------------------------------------------------------------------------------


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def add_entry(request):
    concept = Concept.objects.filter(
        kind="list_type", slug=request.GET.get("type") or request.POST.get("type", "")
    ).first()
    fields = []
    if concept and concept.template_id:
        fields = list(
            AddonField.objects.filter(template_id=concept.template_id, deprecated_at__isnull=True).order_by("id")
        )
    errors, post = [], request.POST
    if request.method == "POST" and concept:
        place = Place.objects.filter(uid=post.get("place", ""), status="active").first()
        name = post.get("name", "").strip()
        if not post.get("rights"):
            errors.append(("rights", "Confirm that you have the right to share this information."))
        if not name:
            errors.append(("name", "Enter the business name."))
        if place is None or place.level == "world":
            errors.append(("place", "Choose a place."))
        addons = {}
        for f in fields:
            raw = post.get(f"addon_{f.key}", "").strip()
            if raw == "":
                continue
            if f.type == "bool":
                addons[f.key] = raw == "yes"
            elif f.type == "number":
                try:
                    addons[f.key] = int(raw)
                except ValueError:
                    errors.append((f"addon_{f.key}", f"{f.key}: enter a whole number."))
            elif f.type == "concept_list":
                addons[f.key] = [s.strip() for s in raw.split(",") if s.strip()]
            else:
                addons[f.key] = raw
        entity = post.get("entity_type", "business")
        if (
            entity == "person"
            and not CountrySwitch.for_country(place.country_code if place else "").named_individuals_on
        ):
            errors.append(("entity_type", "Listing individuals is not open in this country yet."))
        if not errors:
            contacts = [(k, post.get(k, "").strip()) for k in ("phone", "email") if post.get(k, "").strip()]
            try:
                entry = es.create_entry(
                    name=name,
                    place=place,
                    primary_concept=concept,
                    created_by=request.user,
                    website=post.get("website", "").strip(),
                    address_text=post.get("address", "").strip(),
                    contacts=contacts,
                    entity_type=entity,
                    addons=addons,
                )
            except es.EntryError as exc:
                errors.append(("name", str(exc)))
            else:
                prof = ensure_profile(request.user)
                if prof.declared_rights_at is None:
                    prof.declared_rights_at = timezone.now()
                    prof.save(update_fields=["declared_rights_at"])
                return _page(
                    request,
                    "accounts/message.html",
                    {
                        "heading": "Entry added",
                        "body": f"{entry.name} is saved as a draft. It appears on the list after it has been checked.",
                    },
                )
    return _page(
        request,
        "catalog/forms/add_entry.html",
        {
            "concept": concept,
            "list_types": _list_types(),
            "places": _places(),
            "fields": fields,
            "errors": errors,
            "form": post,
        },
    )


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def add_area(request):
    errors, result = [], None
    if request.method == "POST":
        parent = Place.objects.filter(uid=request.POST.get("parent", ""), status="active").first()
        name = request.POST.get("name", "").strip()
        if parent is None or not name:
            errors.append(("name", "Choose the city and enter the area name."))
        else:
            result = propose_area(
                parent=parent, name=name, language=getattr(request, "lang", "en"), proposer=request.user
            )
    return _page(request, "catalog/forms/add_area.html", {"places": _places(), "errors": errors, "result": result})


# ---- claim ---------------------------------------------------------------------------------------------------------


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def claim(request, uid):
    entry = _entry_or_404(uid, published_only=False)  # owners may claim a draft to confirm and correct it
    contacts = list(entry.contact_set.all())
    channels = sorted({("email" if c.kind == "email" else "phone") for c in contacts})
    ctx = {"entry": entry, "channels": channels, "step": "choose", "errors": []}
    if entry.claim_state == "claimed":
        return _page(
            request,
            "accounts/message.html",
            {"heading": "Already claimed", "body": "This business has an owner. Use Something wrong to dispute it."},
        )
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "send":
            channel = request.POST.get("channel")
            pool = [c for c in contacts if (c.kind == "email") == (channel == "email")]
            if not pool:
                ctx["errors"].append(("channel", "No contact of that kind is stored."))
            else:
                try:
                    relay.send_claim_otp(entry, request.user, pool[0])
                    ctx["step"] = "code"
                except relay.RelayError as exc:
                    ctx["errors"].append(("channel", str(exc)))
        elif action == "verify":
            ctx["step"] = "code"
            if not request.POST.get("optin"):  # checked first so a missing tick never burns the code
                ctx["errors"].append(
                    ("optin", "Tick the box to receive enquiries through AllLists, or send documents instead.")
                )
            else:
                contact = relay.verify_claim_otp(entry, request.user, request.POST.get("code", ""))
                if contact is None:
                    ctx["errors"].append(("code", "That code is wrong or has expired."))
                else:
                    try:
                        c = es.start_claim(
                            entry,
                            request.user,
                            "otp_phone" if contact.kind != "email" else "otp_email",
                            "code verified on a stored contact",
                        )
                        es.approve_claim_by_code(c, contact)
                    except es.EntryError as exc:
                        ctx["errors"].append(("code", str(exc)))
                    else:
                        return _page(
                            request,
                            "accounts/message.html",
                            {
                                "heading": "You now own this listing",
                                "body": "Your listing shows an Owner-verified check. Enquiries reach you by email.",
                            },
                        )
        elif action == "documents":
            text = request.POST.get("evidence", "").strip()
            if len(text) < 20:
                ctx["errors"].append(("evidence", "Describe how you run this business (at least a sentence)."))
            else:
                es.start_claim(entry, request.user, "documents", text[:2000])
                return _page(
                    request,
                    "accounts/message.html",
                    {"heading": "Claim received", "body": "A moderator will review it."},
                )
    return _page(request, "catalog/forms/claim.html", ctx)


# ---- something wrong ------------------------------------------------------------------------------------------------


@require_http_methods(["GET", "POST"])
def wrong(request, uid):
    entry = Entry.objects.filter(uid=uid, deleted_at__isnull=True).select_related("place").first()
    if entry is None or entry.publish_state == "tombstoned":
        raise Http404
    errors = []
    if request.method == "POST":
        if request.POST.get("website2"):  # honeypot
            return _page(request, "accounts/message.html", {"heading": "Thank you", "body": "We will look into it."})
        kind = request.POST.get("kind", "")
        text = request.POST.get("text", "").strip()
        if kind not in {k for k, _ in WRONG_KINDS}:
            errors.append(("kind", "Choose what is wrong."))
        elif kind != "remove_my_data" and len(text) < 5:
            errors.append(("text", "Tell us what is wrong."))
        if not errors:
            try:
                mod.submit_report(
                    entry, kind, text, address=throttle.client_address(request), contact=request.POST.get("contact", "")
                )
            except mod.ModerationError as exc:
                errors.append(("kind", str(exc)))
            else:
                msg = (
                    "We received your request to remove or correct your data. It is free and we will act within 30 days."
                    if kind == "remove_my_data"
                    else "Thank you. A moderator will check it."
                )
                return _page(request, "accounts/message.html", {"heading": "Received", "body": msg})
    return _page(
        request,
        "catalog/forms/wrong.html",
        {"entry": entry, "kinds": WRONG_KINDS, "errors": errors, "form": request.POST},
    )


WRONG_KINDS = [
    ("closed", "It has closed or moved"),
    ("wrong", "Something is wrong"),
    ("duplicate", "It is listed twice"),
    ("fake", "It looks fake"),
    ("suggest_edit", "I want to suggest a correction"),
    ("remove_my_data", "Remove or correct my personal data"),
]


# ---- messages and enquiries -------------------------------------------------------------------------------------------


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def message(request, uid):
    entry = _entry_or_404(uid)
    if entry.status == "permanently_closed":
        raise Http404
    errors = []
    if request.method == "POST":
        try:
            enq, counts = relay.send_enquiry(
                request.user, [entry], request.POST.get("text", ""), request.POST.get("reply_to") or request.user.email
            )
        except relay.RelayError as exc:
            errors.append(("text", str(exc)))
        else:
            sent = counts["delivered"] + counts["queued"]
            body = (
                "Your message was passed on. Replies reach you by email."
                if sent
                else "This business has not opted in to receive messages through AllLists yet. Your message was not sent."
            )
            return _page(request, "accounts/message.html", {"heading": "Message", "body": body})
    return _page(request, "catalog/forms/message.html", {"entry": entry, "errors": errors, "form": request.POST})


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def enquiry_many(request):
    place = Place.objects.filter(path=request.GET.get("path") or request.POST.get("path", ""), status="active").first()
    concept = Concept.objects.filter(
        kind="list_type", slug=request.GET.get("type") or request.POST.get("type", "")
    ).first()
    if place is None or concept is None:
        raise Http404
    viewer = Viewer(scopes=tuple(access_services.active_scopes(request.user)))
    if not subscribes_to(viewer, place.path, concept.pk) and not has_cap(request.user, "moderate"):
        return _page(
            request,
            "accounts/message.html",
            {"heading": "Subscribers only", "body": "Sending one message to several businesses is for subscribers."},
            status=403,
        )
    entries = list(queries.published_entries(place, concept).order_by("name_fold")[:50])
    errors = []
    if request.method == "POST":
        ids = set(request.POST.getlist("entry"))
        chosen = [e for e in entries if e.uid in ids]
        try:
            enq, counts = relay.send_enquiry(
                request.user,
                chosen,
                request.POST.get("text", ""),
                request.POST.get("reply_to") or request.user.email,
                allow_many=True,
                scope_path=place.path,
            )
        except relay.RelayError as exc:
            errors.append(("text", str(exc)))
        else:
            return redirect(f"/account/enquiries/#e{enq.pk}")
    return _page(
        request,
        "catalog/forms/enquiry_many.html",
        {"place": place, "concept": concept, "entries": entries, "errors": errors},
    )


@login_required(login_url=LOGIN)
def my_enquiries(request):
    rows = []
    for enq in Enquiry.objects.filter(sender=request.user).order_by("-id")[:50]:
        c = {"delivered": 0, "queued": 0, "not_reachable": 0, "suppressed": 0}
        for r in enq.recipients.all():
            c[r.state] += 1
        rows.append({"enq": enq, "counts": c})
    return _page(request, "catalog/forms/my_enquiries.html", {"rows": rows})


@require_http_methods(["GET", "POST"])
def optout(request, token):
    contact = relay.contact_from_optout_token(token)
    if contact is None:
        raise Http404
    if request.method == "POST":
        relay.opt_out(contact)
        return _page(
            request,
            "accounts/message.html",
            {"heading": "You will not be contacted again", "body": "Your choice takes effect immediately."},
        )
    return _page(request, "catalog/forms/optout.html", {"token": token})


# ---- owner page: company sections and certificates ---------------------------------------------------------------------


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def owner_page(request, uid):
    entry = _entry_or_404(uid, published_only=False)
    if not es.is_owner(entry, request.user):
        raise Http404
    errors, saved = [], False
    active = es.company_page_active(entry) and es.company_page_allowed(entry)
    if request.method == "POST" and active:
        action = request.POST.get("action")
        try:
            if action == "section":
                es.save_company_section(
                    entry,
                    request.user,
                    request.POST.get("kind", ""),
                    request.POST.get("body", ""),
                    title=request.POST.get("title", ""),
                    section_id=int(request.POST["section_id"]) if request.POST.get("section_id") else None,
                )
                saved = True
            elif action == "certificate":
                scheme, value = request.POST.get("scheme", "").strip(), request.POST.get("value", "").strip()
                if not scheme or not value or len(value) > 80:
                    raise es.EntryError("enter the certificate name and number")
                from entries.models import Identifier

                Identifier.objects.create(
                    entry=entry,
                    country_code=entry.country_code,
                    scheme=scheme[:30],
                    value=value,
                    issuer=request.POST.get("issuer", "")[:120],
                )
                saved = True
        except (es.EntryError, ValueError) as exc:
            errors.append(("body", str(exc)))
    return _page(
        request,
        "catalog/forms/owner.html",
        {
            "entry": entry,
            "active": active,
            "eligible": es.company_page_allowed(entry),
            "sections": entry.company_sections.order_by("kind", "sort", "id"),
            "certs": entry.identifier_set.all(),
            "kinds": es.COMPANY_KINDS,
            "errors": errors,
            "saved": saved,
        },
    )
