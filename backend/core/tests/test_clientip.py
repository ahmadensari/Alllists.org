from django.test import RequestFactory, override_settings

from core.clientip import client_address


def _req(**meta):
    return RequestFactory().get("/", **meta)


@override_settings(BEHIND_CLOUDFLARE=False)
def test_header_ignored_when_not_behind_cloudflare():
    assert client_address(_req(REMOTE_ADDR="10.0.0.1", HTTP_CF_CONNECTING_IP="9.9.9.9")) == "10.0.0.1"


@override_settings(BEHIND_CLOUDFLARE=True)
def test_header_used_behind_cloudflare_and_falls_back():
    assert client_address(_req(REMOTE_ADDR="10.0.0.1", HTTP_CF_CONNECTING_IP="9.9.9.9")) == "9.9.9.9"
    assert client_address(_req(REMOTE_ADDR="10.0.0.1")) == "10.0.0.1"
