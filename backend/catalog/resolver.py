"""Address resolution (plan 8.2): the last segment is a place if a child place has that slug, else a list type."""

from places.models import Place
from taxonomy.models import Concept


def place_url(place):
    return "/" if not place.path else "/" + place.path.replace(".", "/") + "/"


def list_url(place, concept):
    return place_url(place) + concept.slug + "/"


def world():
    return Place.objects.filter(level=Place.Level.WORLD, status="active").first()


def resolve(path):
    """Return ("place", place), ("list", place, concept) or None for an address path without slashes at the ends."""
    segments = [s for s in path.strip("/").split("/") if s]
    if not segments:
        w = world()
        return ("place", w) if w else None
    dotted = ".".join(segments)
    place = Place.objects.filter(path=dotted, status="active").first()
    if place:
        return ("place", place)
    if len(segments) >= 2:
        parent = Place.objects.filter(path=".".join(segments[:-1]), status="active").first()
    else:
        parent = world()
    if parent:
        concept = Concept.objects.filter(kind=Concept.Kind.LIST_TYPE, slug=segments[-1], status="active").first()
        if concept:
            return ("list", parent, concept)
    return None
