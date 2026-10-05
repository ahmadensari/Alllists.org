"""Licence gate (rules R21, R22). A blocked source can never feed a published record."""
from .models import Source


class SourceBlocked(Exception):
    pass


def assert_allowed(source, use):
    """Raise SourceBlocked unless `source` may be used for `use` ("import", "agent_fetch", "display")."""
    if source is None:
        raise SourceBlocked("every record needs a source")
    if source.status != "active":
        raise SourceBlocked(f"source {source.name!r} is not active")
    if source.tier == Source.Tier.RED:
        raise SourceBlocked(f"source {source.name!r} is red (scraping, logins or bought lists are never ingested)")
    if use not in (source.allowed_uses or []):
        raise SourceBlocked(f"source {source.name!r} does not allow {use!r}")
    if use == "import" and source.tier == Source.Tier.AMBER and not source.reviewed_on:
        raise SourceBlocked(f"amber source {source.name!r} has no recorded terms review")
    return True
