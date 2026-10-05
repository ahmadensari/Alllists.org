"""Where the viewer is: the chosen place, else the edge guess, else nothing (plan 10.2). Used only by fragments."""

from core.textfold import fold
from places.models import Place, PlaceName


def guess_place(country_code, city_name):
    """Match the CDN's country and city headers to the place tree. Falls back to the country, then to None."""
    country_code = (country_code or "").upper()[:2]
    if not country_code or country_code in ("XX", "T1"):
        return None
    if city_name:
        hit = (
            PlaceName.objects.filter(
                name_fold=fold(city_name), place__country_code=country_code, place__level="city", place__status="active"
            )
            .select_related("place")
            .first()
        )
        if hit:
            return hit.place
    return Place.objects.filter(country_code=country_code, level="country", status="active").first()


def viewer_place(request):
    """Return (place, source) with source in chosen, guess or none."""
    pid = request.session.get("place_uid")
    if pid:
        place = Place.objects.filter(uid=pid, status="active").first()
        if place:
            return place, "chosen"
    place = guess_place(request.META.get("HTTP_CF_IPCOUNTRY", ""), request.META.get("HTTP_CF_IPCITY", ""))
    return (place, "guess") if place else (None, "none")
