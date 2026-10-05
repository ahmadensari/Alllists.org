from django.db import transaction
from django.utils.text import slugify

from core.models import audit
from core.textfold import fold
from taxonomy.models import ReservedSlug

from .models import Place, PlaceName, PlaceProposal


class PlaceError(ValueError):
    pass


def make_slug(name):
    slug = slugify(name, allow_unicode=False)
    if not slug:
        raise PlaceError("a place needs an ASCII slug; transliterate the name first")
    return slug


@transaction.atomic
def create_place(*, parent, level, name, language="en", slug=None, country_code="", names=None, actor=None, **extra):
    """Create a place, keeping `path`, `depth` and `country_code` consistent. `names` is a list of (language, name)."""
    slug = slug or make_slug(name)
    if parent is not None and parent.country_code and not country_code:
        country_code = parent.country_code
    if level == Place.Level.COUNTRY and not country_code:
        raise PlaceError("a country needs a country_code")
    if ReservedSlug.objects.filter(slug=slug, kind="list_type").exists():
        raise PlaceError(f"slug {slug!r} is reserved by a list type")
    path = slug if parent is None or not parent.path else f"{parent.path}.{slug}"
    if level == Place.Level.WORLD:
        path = ""
    if level == Place.Level.COUNTRY:
        path = country_code.lower()
        slug = country_code.lower()
    place = Place.objects.create(parent=parent, level=level, slug=slug, path=path,
                                 depth=0 if parent is None else parent.depth + 1,
                                 country_code=country_code.upper(), **extra)
    ReservedSlug.objects.get_or_create(slug=slug, kind="place")
    for lang, nm in [(language, name)] + list(names or []):
        PlaceName.objects.create(place=place, language=lang, name=nm, name_fold=fold(nm))
    audit("place.create", actor=actor, object_type="place", object_uid=place.uid, country_code=place.country_code)
    return place


def descendants(place):
    """Everything under a place: one prefix range scan on `path`."""
    if not place.path:
        return Place.objects.exclude(pk=place.pk)
    return Place.objects.filter(path__startswith=place.path + ".")


def propose_area(*, parent, name, language="en", proposer=None):
    """Match against existing areas first; a close match is returned as a duplicate hint."""
    folded = fold(name)
    existing = Place.objects.filter(parent=parent, names__name_fold=folded).first()
    prop = PlaceProposal.objects.create(parent=parent, proposed_name=name, language=language,
                                        proposer_id=getattr(proposer, "pk", None),
                                        state=PlaceProposal.State.DUPLICATE if existing else PlaceProposal.State.PENDING,
                                        duplicate_of=existing)
    return prop


@transaction.atomic
def approve_proposal(proposal, *, actor, level=Place.Level.AREA, slug=None):
    if proposal.state != PlaceProposal.State.PENDING:
        raise PlaceError("only pending proposals can be approved")
    place = create_place(parent=proposal.parent, level=level, name=proposal.proposed_name,
                         language=proposal.language, slug=slug, actor=actor)
    proposal.state = PlaceProposal.State.APPROVED
    proposal.decided_by = getattr(actor, "pk", None)
    proposal.save(update_fields=["state", "decided_by"])
    return place
