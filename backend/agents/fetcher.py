"""Fetching for agents (plan 7.6, 17.2): honest user agent, robots respected, private addresses blocked (SSRF), size and
time caps, per-site rate limit, stop at the first refusal."""

import ipaddress
import socket
import threading
import time
from dataclasses import dataclass
from urllib import robotparser
from urllib.parse import urlparse

USER_AGENT = "AllListsBot/1.0 (+https://alllists.com/sources/)"
MAX_BYTES = 500_000
TIMEOUT = 10
MIN_INTERVAL = 2.0


class FetchRefused(Exception):
    """Raised when robots, the address, or the site says no. The job stops."""


@dataclass
class FetchResult:
    url: str
    status: int
    text: str


_local = threading.local()
_real_getaddrinfo = socket.getaddrinfo


def _pinned_getaddrinfo(host, *args, **kwargs):
    """Name lookups behave normally, except for the one host a fetch has already checked: that host resolves to the
    address that was checked, so a name that changes its answer between the check and the connection (DNS rebinding)
    cannot lead the request to a private address."""
    pin = getattr(_local, "pin", None)
    if pin and host == pin[0]:
        port = args[0] if args and args[0] else 0
        if ":" in pin[1]:
            return [(socket.AF_INET6, socket.SOCK_STREAM, 6, "", (pin[1], port, 0, 0))]
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (pin[1], port))]
    return _real_getaddrinfo(host, *args, **kwargs)


socket.getaddrinfo = _pinned_getaddrinfo


_NAT64 = ipaddress.ip_network("64:ff9b::/96")
_SIX_TO_FOUR = ipaddress.ip_network("2002::/16")
_TEREDO = ipaddress.ip_network("2001::/32")


def _is_public_ip(raw):
    ip = ipaddress.ip_address(raw)
    if ip.version == 6:
        if ip.ipv4_mapped is not None:
            ip = ip.ipv4_mapped  # ::ffff:127.0.0.1 is loopback in disguise
        elif ip in _NAT64:
            ip = ipaddress.ip_address(int(ip) & 0xFFFFFFFF)  # an IPv4 address carried inside the NAT64 prefix
        elif ip in _SIX_TO_FOUR:
            ip = ipaddress.ip_address((int(ip) >> 80) & 0xFFFFFFFF)  # IPv4 address carried by 6to4
        elif ip in _TEREDO:
            return False
    return ip.is_global and not (ip.is_multicast or ip.is_unspecified)


def resolve_public(host):
    """The first address of `host` when EVERY address it resolves to is public, else None."""
    try:
        infos = _real_getaddrinfo(host, None)
    except (socket.gaierror, UnicodeError):
        return None
    addrs = [i[4][0].split("%")[0] for i in infos]
    if not addrs or not all(_is_public_ip(a) for a in addrs):
        return None
    return addrs[0]


def is_public_address(host):
    """True only when every address the name resolves to is public. Blocks loopback, private, link-local, shared (CGNAT),
    reserved, multicast and unspecified addresses, and IPv4 addresses hidden inside IPv6."""
    return resolve_public(host) is not None


def check_url(url):
    return _check(url)[0]


def _check(url):
    """Validate an address and resolve it once. Returns (parsed url, the public address that was checked)."""
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise FetchRefused("only http and https addresses are fetched")
    if p.username or p.password:
        raise FetchRefused("addresses with credentials are refused")
    try:
        port = p.port
    except ValueError as exc:
        raise FetchRefused("bad port") from exc
    if port not in (None, 80, 443):
        raise FetchRefused("only ports 80 and 443 are fetched")
    ip = resolve_public(p.hostname)
    if ip is None:
        raise FetchRefused("address is not public")
    return p, ip


class HttpFetcher:
    def __init__(self, http=None):
        self._last = {}
        self._robots = {}
        self._http = http  # anything with .get(url, headers=, timeout=, stream=, allow_redirects=); tests pass a fake

    def _client(self):
        if self._http is None:
            import requests  # imported late: only the real fetcher needs the network library

            self._http = requests
        return self._http

    def _robots_for(self, p):
        """robots.txt is fetched like any page: public address, no redirects, size cap. No readable file (an error, a
        redirect, a refusal) means no permission; a plain 404 means no rules."""
        base = f"{p.scheme}://{p.netloc}"
        rp = self._robots.get(base)
        if rp is not None:
            return rp
        rp = robotparser.RobotFileParser()
        rp.set_url(base + "/robots.txt")
        try:
            r = self._client().get(
                base + "/robots.txt",
                headers={"User-Agent": USER_AGENT},
                timeout=TIMEOUT,
                stream=True,
                allow_redirects=False,
            )
            if r.status_code in (404, 410):
                rp.allow_all = True
            elif r.status_code != 200:
                rp.disallow_all = True
            else:
                body = r.raw.read(MAX_BYTES + 1, decode_content=True)
                if len(body) > MAX_BYTES:
                    rp.disallow_all = True
                else:
                    rp.parse(body.decode("utf-8", errors="replace").splitlines())
        except Exception:  # noqa: BLE001 - any failure means no permission
            rp.disallow_all = True
        self._robots[base] = rp
        return rp

    def _allowed(self, p):
        return self._robots_for(p).can_fetch(USER_AGENT, p.geturl())

    def get(self, url):
        p, ip = _check(url)  # one lookup: the address checked is the address that will be used
        _local.pin = (p.hostname, ip)
        try:
            if not self._allowed(p):
                raise FetchRefused("robots.txt does not allow this page")
            wait = MIN_INTERVAL - (time.monotonic() - self._last.get(p.netloc, 0))
            if wait > 0:
                time.sleep(wait)
            self._last[p.netloc] = time.monotonic()
            r = self._client().get(
                url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, stream=True, allow_redirects=False
            )
            if r.status_code in (301, 302, 303, 307, 308):
                raise FetchRefused("redirects are not followed; fetch the final address")
            if r.status_code in (401, 403, 429):
                raise FetchRefused(f"site refused with {r.status_code}")
            body = r.raw.read(MAX_BYTES + 1, decode_content=True)
            if len(body) > MAX_BYTES:
                raise FetchRefused("page too large")
            return FetchResult(url, r.status_code, body.decode(r.encoding or "utf-8", errors="replace"))
        finally:
            _local.pin = None


class FakeFetcher:
    """For tests and dry runs: serves pages from a dict and records every request."""

    def __init__(self, pages=None, refuse=()):
        self.pages, self.refuse, self.requested = dict(pages or {}), set(refuse), []

    def get(self, url):
        self.requested.append(url)
        if url in self.refuse:
            raise FetchRefused("refused")
        return FetchResult(url, 200, self.pages.get(url, ""))
