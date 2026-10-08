import datetime

import pytest

from intake.gate import SourceBlocked, assert_allowed
from intake.models import Source


def mk(**kw):
    base = dict(name="s", tier="green", allowed_uses=["import", "display"])
    base.update(kw)
    return Source(**base)


def test_red_source_always_blocked():
    for use in ("import", "agent_fetch", "display"):
        with pytest.raises(SourceBlocked):
            assert_allowed(mk(tier="red", allowed_uses=["import", "agent_fetch", "display"]), use)


def test_missing_source_and_unallowed_use_blocked():
    with pytest.raises(SourceBlocked):
        assert_allowed(None, "import")
    with pytest.raises(SourceBlocked):
        assert_allowed(mk(), "agent_fetch")
    with pytest.raises(SourceBlocked):
        assert_allowed(mk(status="paused"), "import")


def test_amber_import_needs_a_terms_review():
    with pytest.raises(SourceBlocked):
        assert_allowed(mk(tier="amber"), "import")
    assert assert_allowed(mk(tier="amber", reviewed_on=datetime.date(2026, 10, 1)), "import")


def test_green_allowed():
    assert assert_allowed(mk(), "import")
