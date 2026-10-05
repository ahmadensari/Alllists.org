"""Fetching for agents (plan 7.6, 17.2): honest user agent, robots respected, private addresses blocked (SSRF), size and
time caps, per-site rate limit, stop at the first refusal."""

import ipaddress
import socket
import time
from dataclasses import dataclass
from urllib import robotparser
from urllib.parse import urlparse

USER_AGENT = "AllListsBot/1.0 (+https://alllists.org/sources/)"
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


def is_public_address(host):
    """True only when every address the name resolves to is public. Blocks loopback, private, link-local and reserved."""
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ):
            return False
    return bool(infos)


def check_url(url):
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise FetchRefused("only http and https addresses are fetched")
    if p.username or p.password:
        raise FetchRefused("addresses with credentials are refused")
    if not is_public_address(p.hostname):
        raise FetchRefused("address is not public")
    return p


class HttpFetcher:
    def __init__(self):
        self._last = {}
        self._robots = {}

    def _allowed(self, p):
        base = f"{p.scheme}://{p.netloc}"
        rp = self._robots.get(base)
        if rp is None:
            rp = robotparser.RobotFileParser()
            rp.set_url(base + "/robots.txt")
            try:
                rp.read()
            except Exception:
                rp.disallow_all = True  # no readable robots file means no permission
            self._robots[base] = rp
        return rp.can_fetch(USER_AGENT, p.geturl())

    def get(self, url):
        import requests  # imported late: only the real fetcher needs the network library

        p = check_url(url)
        if not self._allowed(p):
            raise FetchRefused("robots.txt does not allow this page")
        wait = MIN_INTERVAL - (time.monotonic() - self._last.get(p.netloc, 0))
        if wait > 0:
            time.sleep(wait)
        self._last[p.netloc] = time.monotonic()
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, stream=True, allow_redirects=False)
        if r.status_code in (301, 302, 303, 307, 308):
            raise FetchRefused("redirects are not followed; fetch the final address")
        if r.status_code in (401, 403, 429):
            raise FetchRefused(f"site refused with {r.status_code}")
        body = r.raw.read(MAX_BYTES + 1, decode_content=True)
        if len(body) > MAX_BYTES:
            raise FetchRefused("page too large")
        return FetchResult(url, r.status_code, body.decode(r.encoding or "utf-8", errors="replace"))


class FakeFetcher:
    """For tests and dry runs: serves pages from a dict and records every request."""

    def __init__(self, pages=None, refuse=()):
        self.pages, self.refuse, self.requested = dict(pages or {}), set(refuse), []

    def get(self, url):
        self.requested.append(url)
        if url in self.refuse:
            raise FetchRefused("refused")
        return FetchResult(url, 200, self.pages.get(url, ""))
