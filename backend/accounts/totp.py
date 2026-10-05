"""RFC 6238 time-based one-time passwords with the standard library (no extra dependency)."""

import base64
import hashlib
import hmac
import os
import struct
import time
from urllib.parse import quote


def new_secret():
    return base64.b32encode(os.urandom(20)).decode().rstrip("=")


def hotp(secret, counter, digits=6):
    key = base64.b32decode(secret + "=" * (-len(secret) % 8), casefold=True)
    mac = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    off = mac[-1] & 0x0F
    code = (struct.unpack(">I", mac[off : off + 4])[0] & 0x7FFFFFFF) % (10**digits)
    return str(code).zfill(digits)


def totp(secret, at=None, step=30, digits=6):
    return hotp(secret, int((at if at is not None else time.time()) // step), digits)


def verify(secret, code, at=None, step=30, window=1, last_step=0):
    """Return the matched time step (to store against replay) or None."""
    code = (code or "").strip().replace(" ", "")
    now_step = int((at if at is not None else time.time()) // step)
    for s in range(now_step - window, now_step + window + 1):
        if s > last_step and hmac.compare_digest(hotp(secret, s), code):
            return s
    return None


def provisioning_uri(secret, account, issuer="AllLists"):
    return f"otpauth://totp/{quote(issuer)}:{quote(account)}?secret={secret}&issuer={quote(issuer)}"
