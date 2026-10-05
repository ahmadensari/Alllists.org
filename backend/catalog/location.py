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


def nearest_place(lat, lon, max_km=60):
    """The closest active place (city or smaller) with a stored centre, within `max_km`. Used by the exact-location button.
    Uses a bounding box first and haversine distance second (PostGIS replaces this at stage S1)."""
    import math

    lat, lon = float(lat), float(lon)
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    box = max_km / 111.0
    qs = Place.objects.filter(
        status="active",
        centre_lat__isnull=False,
        level__in=["city", "area", "society", "street"],
        centre_lat__gte=lat - box,
        centre_lat__lte=lat + box,
        centre_lon__gte=lon - box * 1.5,
        centre_lon__lte=lon + box * 1.5,
    )
    best, best_d = None, None
    for p in qs:
        p1, p2 = math.radians(lat), math.radians(float(p.centre_lat))
        dl = math.radians(float(p.centre_lon) - lon)
        h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
        d = 2 * 6371.0 * math.asin(math.sqrt(h))
        if d <= max_km and (best_d is None or d < best_d or (d == best_d and p.depth > best.depth)):
            best, best_d = p, d
    return best
