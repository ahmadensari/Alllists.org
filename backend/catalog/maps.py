"""Map links are built at display time from the stored WGS-84 point (rule R36). China uses shifted systems: Amap uses
GCJ-02 and Baidu BD-09, so conversion happens here and never in stored data."""

import math
from urllib.parse import quote

_A = 6378245.0
_EE = 0.00669342162296594323
_X_PI = math.pi * 3000.0 / 180.0


def out_of_china(lat, lon):
    return not (73.66 < lon < 135.05 and 3.86 < lat < 53.55)


def _tlat(x, y):
    r = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    r += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    r += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return r


def _tlon(x, y):
    r = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    r += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    r += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return r


def wgs84_to_gcj02(lat, lon):
    if out_of_china(lat, lon):
        return lat, lon
    dlat, dlon = _tlat(lon - 105.0, lat - 35.0), _tlon(lon - 105.0, lat - 35.0)
    rad = lat / 180.0 * math.pi
    magic = 1 - _EE * math.sin(rad) ** 2
    sq = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((_A * (1 - _EE)) / (magic * sq) * math.pi)
    dlon = (dlon * 180.0) / (_A / sq * math.cos(rad) * math.pi)
    return lat + dlat, lon + dlon


def gcj02_to_bd09(lat, lon):
    z = math.sqrt(lon * lon + lat * lat) + 0.00002 * math.sin(lat * _X_PI)
    theta = math.atan2(lat, lon) + 0.000003 * math.cos(lon * _X_PI)
    return z * math.sin(theta) + 0.006, z * math.cos(theta) + 0.0065


def links(lat, lon, country_code=""):
    """Return {name: url} for a stored point. Baidu and Amap appear for China only."""
    lat, lon = float(lat), float(lon)
    out = {
        "google": f"https://www.google.com/maps/search/?api=1&query={lat:.6f},{lon:.6f}",
        "apple": f"https://maps.apple.com/?ll={lat:.6f},{lon:.6f}&q={quote('Pin')}",
        "osm": f"https://www.openstreetmap.org/?mlat={lat:.6f}&mlon={lon:.6f}#map=18/{lat:.6f}/{lon:.6f}",
    }
    if country_code.upper() == "CN":
        glat, glon = wgs84_to_gcj02(lat, lon)
        blat, blon = gcj02_to_bd09(glat, glon)
        out["amap"] = f"https://uri.amap.com/marker?position={glon:.6f},{glat:.6f}"
        out["baidu"] = f"https://api.map.baidu.com/marker?location={blat:.6f},{blon:.6f}&output=html"
    return out
