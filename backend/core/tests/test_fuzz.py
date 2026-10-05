"""Property and fuzz tests for everything that parses what a stranger types: names, contacts, messages, CSV, URLs,
one-time codes. The properties are the promises the rest of the system leans on."""

import re
import unicodedata

import pytest
from django.test import Client
from hypothesis import HealthCheck, given, settings as hs, strategies as st

from accounts import totp
from core.crypto import decrypt, encrypt
from core.logscrub import scrub
from core.textfold import fold
from entries.services import normalize_contact
from intake import importer
from outreach.services import contact_leaks

ANY_TEXT = st.text(max_size=200)
URDU = st.text(alphabet=st.characters(min_codepoint=0x0600, max_codepoint=0x06FF), max_size=60)


# ---- folding ---------------------------------------------------------------------------------------------------------------


@given(ANY_TEXT)
@hs(max_examples=300, deadline=None)
def test_fold_never_fails_is_idempotent_and_has_no_stray_whitespace(text):
    f = fold(text)
    assert isinstance(f, str) and fold(f) == f
    assert f == f.strip() and "  " not in f


@given(URDU)
@hs(max_examples=200, deadline=None)
def test_arabic_and_urdu_letter_forms_fold_together(text):
    arabic = text.replace("ی", "ي").replace("ک", "ك")
    assert fold(arabic) == fold(text)


def test_fold_known_cases():
    assert fold("كريسنت") == fold("کریسنت")  # Arabic yeh and kaf against the Urdu forms
    assert fold("Crescent  SURGICAL, Works!") == "crescent surgical works"
    assert fold("٠٣٠٠") == fold("0300") == "0300"  # Arabic-Indic digits


# ---- contact safety -----------------------------------------------------------------------------------------------------------


digits = st.sampled_from(list("0123456789") + list("٠١٢٣٤٥٦٧٨٩") + list("۰۱۲۳۴۵۶۷۸۹"))
seps = st.sampled_from([" ", "-", ".", "", "  ", " - ", "()"])


@given(st.lists(st.tuples(digits, seps), min_size=7, max_size=14), st.text(alphabet="abc xyz.", max_size=20))
@hs(max_examples=300, deadline=None)
def test_any_run_of_seven_digits_is_caught_in_any_script_and_spacing(pairs, noise):
    number = "".join(d + s for d, s in pairs)
    assert "a phone number" in contact_leaks(f"{noise} {number} {noise}")


@given(st.text(alphabet=st.characters(whitelist_categories=("L", "Zs"), blacklist_characters="@"), max_size=200))
@hs(max_examples=200, deadline=None)
def test_plain_words_never_trip_the_filter(text):
    unicodedata.normalize("NFC", text)
    if not re.search(r"(?i)www|https?|bit\.ly|t\.me|wa\.me|linktr|tinyurl|goo\.gl|\.[a-z]{2,}", text):
        found = contact_leaks(text)
        assert "a phone number" not in found and "an email address" not in found


@pytest.mark.parametrize(
    "text",
    [
        "call 0300 123 4567",
        "whatsapp +92-300-1234567",
        "my email is bob (at) example (dot) com",
        "bob@example.org",
        "see www.example.org",
        "https://bit.ly/abc",
        "zero three zero zero one two three four five six seven",
        "wa.me/923001234567",
        "t.me/somechannel",
        "٠٣٠٠١٢٣٤٥٦٧٨",
    ],
)
def test_known_ways_to_pass_contacts_are_all_caught(text):
    assert contact_leaks(text), text


@given(ANY_TEXT)
@hs(max_examples=200, deadline=None)
def test_log_scrubber_never_fails_and_removes_emails_and_long_numbers(text):
    scrub(text)
    assert "@x.example" not in scrub(f"{text} bob@x.example")
    assert "0300123456" not in scrub(f"{text} 0300123456")


@given(st.sampled_from(["phone", "email"]), ANY_TEXT)
@hs(max_examples=200, deadline=None)
def test_normalize_contact_never_fails_and_phone_form_is_stable(kind, value):
    once = normalize_contact(kind, value, "PK")
    assert isinstance(once, str)
    assert normalize_contact(kind, once, "PK") == once


def test_pakistani_numbers_have_one_form():
    forms = {
        normalize_contact("phone", v, "PK")
        for v in ("0300 123 4567", "+92 300 1234567", "0092-300-1234567", "(0300)1234567")
    }
    assert forms == {"+923001234567"}


# ---- crypto and one-time codes ---------------------------------------------------------------------------------------------


@given(ANY_TEXT)
@hs(max_examples=100, deadline=None)
def test_encrypt_round_trips_any_text_and_is_never_the_plaintext(text):
    token = encrypt(text)
    assert decrypt(token) == text
    assert len(text) < 8 or text not in token  # short texts can appear by chance inside base64


def test_totp_matches_the_published_rfc_vectors():
    import base64

    secret = base64.b32encode(b"12345678901234567890").decode()
    # RFC 4226 Appendix D (HOTP) and RFC 6238 Appendix B (TOTP, SHA-1, 8 digits)
    assert [totp.hotp(secret, i) for i in range(4)] == ["755224", "287082", "359152", "969429"]
    assert totp.totp(secret, at=59, digits=8) == "94287082"
    assert totp.totp(secret, at=1111111109, digits=8) == "07081804"
    assert totp.totp(secret, at=20000000000, digits=8) == "65353130"


@given(st.text(max_size=30))
@hs(max_examples=200, deadline=None)
def test_wrong_codes_never_verify_and_never_crash(code):
    secret = totp.new_secret()
    good = totp.totp(secret, at=1_700_000_000)
    if code.strip().replace(" ", "") != good:
        assert totp.verify(secret, code, at=1_700_000_000) is None


def test_a_code_works_once_and_only_inside_the_window():
    secret = totp.new_secret()
    at = 1_700_000_000
    code = totp.totp(secret, at=at)
    step = totp.verify(secret, code, at=at)
    assert step is not None
    assert totp.verify(secret, code, at=at, last_step=step) is None  # replay
    assert totp.verify(secret, code, at=at + 31) == step  # one step of clock drift is allowed
    assert totp.verify(secret, code, at=at + 95) is None  # three steps is not


# ---- import parsing ------------------------------------------------------------------------------------------------------------


@given(st.text(max_size=600))
@hs(max_examples=300, deadline=None)
def test_import_parser_never_crashes_on_any_pasted_text(text):
    try:
        headers, rows = importer.parse_table(text)
    except importer.ImportError_:
        return
    mapping = importer.guess_mapping(headers)
    assert set(mapping.values()) <= {"name", "phone", "email", "address", "website", "specialities"}
    for raw in rows[:5]:
        out = importer.normalise_row(raw, mapping, "PK")
        assert isinstance(out["name"], str)


@given(st.lists(st.text(max_size=40), min_size=1, max_size=8))
@hs(max_examples=200, deadline=None)
def test_guess_mapping_is_total(headers):
    m = importer.guess_mapping(headers)
    assert all(h in headers for h in m)


# ---- URLs ----------------------------------------------------------------------------------------------------------------------


segment = st.text(alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="/\x00"), max_size=40)


@given(
    st.lists(segment, min_size=0, max_size=5),
    st.dictionaries(
        st.sampled_from(["q", "area", "sort", "page", "ref", "path", "type", "scope", "next"]), ANY_TEXT, max_size=4
    ),
)
@hs(max_examples=150, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_random_urls_and_queries_never_give_a_server_error(db, tree, surgical, segs, query):
    c = Client(raise_request_exception=False)
    url = "/" + "/".join(segs) + ("/" if segs else "")
    for prefix in ("", "/ur"):
        for target in (
            prefix + url,
            prefix + "/pk/punjab/sialkot/surgical-instrument-makers/",
            prefix + "/search/",
            "/_f/list/",
            "/_f/ref/",
            "/optout/x/",
        ):
            r = c.get(target, query)
            assert r.status_code < 500, (target, query, r.status_code)
