"""The page fetcher is the one place the server makes requests to addresses a stranger supplies, so it is tested hard:
private and disguised addresses, redirects, ports, robots.txt in every state, size caps, and DNS rebinding."""

import io
import socket

import pytest

from agents import fetcher as fe


def resolver(table):
    """A fake DNS: name -> list of addresses, or an exception."""

    def fake(host, *args, **kwargs):
        ans = table.get(host)
        if ans is None:
            raise socket.gaierror("no such host")
        return [(socket.AF_INET6 if ":" in a else socket.AF_INET, socket.SOCK_STREAM, 6, "", (a, 0)) for a in ans]

    return fake


@pytest.fixture
def dns(monkeypatch):
    table = {"public.example": ["93.184.216.34"], "localhost": ["127.0.0.1"]}
    monkeypatch.setattr(fe, "_real_getaddrinfo", resolver(table))
    return table


class Resp:
    def __init__(self, status=200, body=b"", encoding="utf-8"):
        self.status_code, self.encoding = status, encoding
        self.raw = io.BytesIO(body)
        self.raw.read_orig = self.raw.read

        def read(n, decode_content=None):
            assert decode_content is True  # compressed pages are decoded before the size check and parsing
            return self.raw.read_orig(n)

        self.raw.read = read


class Http:
    """Serves canned responses by URL and records every call and the address a lookup gave during the call."""

    def __init__(self, pages):
        self.pages, self.calls, self.lookups = pages, [], []

    def get(self, url, headers=None, timeout=None, stream=None, allow_redirects=None):
        assert allow_redirects is False and timeout and headers["User-Agent"].startswith("AllListsBot")
        assert stream is True  # the body is streamed so a huge page is never loaded in full
        self.calls.append(url)
        host = url.split("/")[2]
        self.lookups.append(socket.getaddrinfo(host, 443)[0][4][0])
        r = self.pages.get(url)
        if isinstance(r, Exception):
            raise r
        return r if r is not None else Resp(404)


ROBOTS_OPEN = Resp(200, b"User-agent: *\nAllow: /\n")


# ---- addresses --------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "addr",
    [
        "127.0.0.1",
        "127.1.2.3",
        "10.0.0.5",
        "172.16.9.9",
        "192.168.1.1",
        "169.254.169.254",  # cloud metadata
        "100.64.0.1",  # shared address space
        "0.0.0.0",
        "224.0.0.1",
        "240.0.0.1",
        "192.0.0.1",
        "198.18.0.1",
        "::1",
        "::",
        "fe80::1",
        "fc00::1",
        "::ffff:127.0.0.1",  # IPv4 loopback written as IPv6
        "::ffff:10.0.0.1",
        "64:ff9b::7f00:1",  # NAT64 carrying 127.0.0.1
        "2002:7f00:1::1",  # 6to4 carrying 127.0.0.1
        "2001:0:4136:e378:8000:63bf:3fff:fdd2",  # Teredo
    ],
)
def test_non_public_addresses_are_refused(dns, addr):
    dns["evil.example"] = [addr]
    assert fe.is_public_address("evil.example") is False
    with pytest.raises(fe.FetchRefused):
        fe.check_url("https://evil.example/page")


def test_public_and_mixed_answers(dns):
    assert fe.is_public_address("public.example")
    dns["both.example"] = ["93.184.216.34", "10.0.0.1"]  # one private answer is enough to refuse
    assert not fe.is_public_address("both.example")
    assert not fe.is_public_address("missing.example")
    dns["v6.example"] = ["2606:2800:220:1:248:1893:25c8:1946"]
    assert fe.is_public_address("v6.example")


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "ftp://public.example/x",
        "gopher://public.example/",
        "javascript:alert(1)",
        "//public.example/x",
        "https://user:pw@public.example/",
        "https://public.example:22/",
        "https://public.example:8080/",
        "https://public.example:abc/",
        "https:///nohost",
        "",
    ],
)
def test_bad_schemes_credentials_and_ports_are_refused(dns, url):
    with pytest.raises(fe.FetchRefused):
        fe.check_url(url)


def test_default_ports_are_fine(dns):
    for u in (
        "https://public.example/",
        "http://public.example/",
        "https://public.example:443/x",
        "http://public.example:80/",
    ):
        assert fe.check_url(u).hostname == "public.example"


@pytest.mark.parametrize(
    "literal", ["http://127.0.0.1/", "http://2130706433/", "http://0x7f.1/", "http://[::1]/", "http://localhost/"]
)
def test_ip_literals_and_odd_spellings_never_pass(monkeypatch, literal):
    # real resolver on purpose: these spellings are resolved by the operating system
    monkeypatch.setattr(
        fe,
        "_real_getaddrinfo",
        socket.getaddrinfo.__wrapped__ if hasattr(socket.getaddrinfo, "__wrapped__") else fe._real_getaddrinfo,
    )
    with pytest.raises(fe.FetchRefused):
        fe.check_url(literal)


# ---- robots and responses -----------------------------------------------------------------------------------------------------


def make(dns, pages):
    http = Http(pages)
    f = fe.HttpFetcher(http=http)
    return f, http


def test_a_normal_page_is_fetched_after_robots(dns, monkeypatch):
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)
    f, http = make(
        dns, {"https://public.example/robots.txt": ROBOTS_OPEN, "https://public.example/p": Resp(200, b"Name: X")}
    )
    r = f.get("https://public.example/p")
    assert r.status == 200 and r.text == "Name: X"
    assert http.calls == ["https://public.example/robots.txt", "https://public.example/p"]


@pytest.mark.parametrize(
    "robots",
    [
        Resp(200, b"User-agent: *\nDisallow: /\n"),
        Resp(200, b"User-agent: AllListsBot\nDisallow: /p\n"),
        Resp(500),
        Resp(503),
        Resp(401),
        Resp(403),
        Resp(301),
        Resp(302),
        RuntimeError("timeout"),
        Resp(200, b"x" * (fe.MAX_BYTES + 5)),
    ],
)
def test_robots_that_forbid_or_cannot_be_read_mean_no(dns, robots):
    f, http = make(dns, {"https://public.example/robots.txt": robots, "https://public.example/p": Resp(200, b"secret")})
    with pytest.raises(fe.FetchRefused, match="robots"):
        f.get("https://public.example/p")
    assert "https://public.example/p" not in http.calls  # the page itself was never requested


def test_missing_robots_file_means_no_rules(dns, monkeypatch):
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)
    f, _ = make(dns, {"https://public.example/robots.txt": Resp(404), "https://public.example/p": Resp(200, b"ok")})
    assert f.get("https://public.example/p").text == "ok"


@pytest.mark.parametrize("status", [301, 302, 303, 307, 308])
def test_redirects_are_never_followed(dns, status, monkeypatch):
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)
    f, http = make(dns, {"https://public.example/robots.txt": ROBOTS_OPEN, "https://public.example/p": Resp(status)})
    with pytest.raises(fe.FetchRefused, match="redirect"):
        f.get("https://public.example/p")
    assert len(http.calls) == 2


@pytest.mark.parametrize("status", [401, 403, 429])
def test_refusal_statuses_stop(dns, status, monkeypatch):
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)
    f, _ = make(dns, {"https://public.example/robots.txt": ROBOTS_OPEN, "https://public.example/p": Resp(status)})
    with pytest.raises(fe.FetchRefused, match=str(status)):
        f.get("https://public.example/p")


def test_oversized_page_is_refused_and_bad_bytes_do_not_crash(dns, monkeypatch):
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)
    f, _ = make(
        dns,
        {
            "https://public.example/robots.txt": ROBOTS_OPEN,
            "https://public.example/big": Resp(200, b"a" * (fe.MAX_BYTES + 1)),
            "https://public.example/bin": Resp(200, b"\xff\xfe\x00bad"),
        },
    )
    with pytest.raises(fe.FetchRefused, match="large"):
        f.get("https://public.example/big")
    assert "bad" in f.get("https://public.example/bin").text


def test_private_target_never_reaches_the_network(dns):
    dns["internal.example"] = ["10.1.1.1"]
    f, http = make(dns, {})
    with pytest.raises(fe.FetchRefused):
        f.get("https://internal.example/admin")
    assert http.calls == []


def test_rate_limit_waits_between_requests_to_one_site(dns, monkeypatch):
    slept = []
    monkeypatch.setattr(fe.time, "sleep", lambda s: slept.append(s))
    pages = {
        "https://public.example/robots.txt": ROBOTS_OPEN,
        "https://public.example/1": Resp(200, b"a"),
        "https://public.example/2": Resp(200, b"b"),
    }
    f, _ = make(dns, pages)
    f.get("https://public.example/1")
    pages["https://public.example/2"] = Resp(200, b"b")
    f.get("https://public.example/2")
    assert slept and 0 < slept[-1] <= fe.MIN_INTERVAL


# ---- DNS rebinding -------------------------------------------------------------------------------------------------------------


def test_name_that_changes_its_answer_after_the_check_cannot_reach_a_private_address(monkeypatch):
    """The first lookup (the check) says public; every later lookup says 127.0.0.1. The connection must still go to the
    address that was checked."""
    answers = iter([["93.184.216.34"]])
    state = {"flip": False}

    def flipping(host, *a, **k):
        addr = "127.0.0.1" if state["flip"] else "93.184.216.34"
        state["flip"] = True
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (addr, 0))]

    monkeypatch.setattr(fe, "_real_getaddrinfo", flipping)
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)
    assert answers
    http = Http({"https://rebind.example/robots.txt": ROBOTS_OPEN, "https://rebind.example/p": Resp(200, b"ok")})
    f = fe.HttpFetcher(http=http)
    f.get("https://rebind.example/p")
    assert set(http.lookups) == {"93.184.216.34"}  # every connection-time lookup was pinned to the checked address


def test_pin_is_cleared_after_every_fetch_even_after_errors(dns, monkeypatch):
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)
    f, _ = make(dns, {"https://public.example/robots.txt": ROBOTS_OPEN, "https://public.example/p": Resp(403)})
    with pytest.raises(fe.FetchRefused):
        f.get("https://public.example/p")
    assert getattr(fe._local, "pin", None) is None
    # outside a fetch, lookups behave normally and are not pinned to anything
    assert fe._pinned_getaddrinfo("localhost", 80)[0][4][0] in ("127.0.0.1", "::1")


def test_pinned_lookup_only_answers_for_the_pinned_name(dns):
    fe._local.pin = ("public.example", "93.184.216.34")
    try:
        assert fe._pinned_getaddrinfo("public.example", 443)[0][4][0] == "93.184.216.34"
        assert fe._pinned_getaddrinfo("localhost", 80)[0][4][0] in ("127.0.0.1", "::1")  # other names resolve normally
        fe._local.pin = ("v6.example", "2606:2800:220:1:248:1893:25c8:1946")
        assert len(fe._pinned_getaddrinfo("v6.example", 443)[0][4]) == 4  # IPv6 socket address shape
    finally:
        fe._local.pin = None


def test_a_page_of_exactly_the_size_limit_is_accepted_and_one_byte_more_is_not(dns, monkeypatch):
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)
    f, _ = make(
        dns,
        {
            "https://public.example/robots.txt": ROBOTS_OPEN,
            "https://public.example/edge": Resp(200, b"a" * fe.MAX_BYTES),
            "https://public.example/over": Resp(200, b"a" * (fe.MAX_BYTES + 1)),
        },
    )
    assert len(f.get("https://public.example/edge").text) == fe.MAX_BYTES
    with pytest.raises(fe.FetchRefused, match="large"):
        f.get("https://public.example/over")
