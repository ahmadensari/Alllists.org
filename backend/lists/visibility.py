"""What a visitor may see. Free: names, area, up to 3 specialities, checks with dates.
Subscriber: also address, exact pin, size, website, social links, markets, MOQ, prices, certificates,
one enquiry to many. Phone, WhatsApp and email are never shown to anyone (outreach relay only)."""
from django.conf import settings

NEVER_SHOWN = ("phone", "whatsapp", "email")


def entry_view(entry, subscriber):
    d = {
        "entry": entry,
        "name": entry.name, "name_alt": entry.name_alt, "type": entry.entry_type,
        "area": entry.place.name, "area_ur": entry.place.name_ur,
        "specialities": list(entry.specialities)[: (None if subscriber else settings.FREE_MAX_SPECIALITIES)],
        "more_specialities": 0 if subscriber else max(0, len(entry.specialities) - settings.FREE_MAX_SPECIALITIES),
        "level": entry.best_level(), "last_checked": entry.last_checked(),
        "status": entry.status, "is_company": entry.is_company, "sponsored": entry.sponsored,
        "locked": not subscriber,
    }
    if subscriber:
        d.update(address=entry.address, latitude=entry.latitude, longitude=entry.longitude,
                 website=entry.website, size=entry.size, markets=entry.markets, moq=entry.moq,
                 price_note=entry.price_note, certificates=entry.certificates,
                 socials=list(entry.socials.all()), services=[s.text for s in entry.services.all()],
                 identifiers=list(entry.identifiers.all()))
        if entry.is_company:
            d["company_profile"] = entry.company_profile
    return d


def name_only(entry):
    return {"entry": entry, "name": entry.name, "name_alt": entry.name_alt, "area": entry.place.name,
            "area_ur": entry.place.name_ur, "level": entry.best_level(), "last_checked": entry.last_checked(),
            "specialities": [], "more_specialities": 0, "locked": True, "names_only": True,
            "is_company": entry.is_company, "sponsored": entry.sponsored, "status": entry.status}
