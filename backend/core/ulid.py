"""ULID: 26 characters, time-ordered, never reused. Public ids in URLs (plan section 4.1)."""

import os
import time

_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def new_ulid(now_ms=None):
    ms = int(time.time() * 1000) if now_ms is None else now_ms
    value = (ms << 80) | int.from_bytes(os.urandom(10), "big")
    out = []
    for _ in range(26):
        out.append(_ALPHABET[value & 31])
        value >>= 5
    return "".join(reversed(out))
