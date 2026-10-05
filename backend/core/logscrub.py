"""Log scrubber (plan 17.2): no contact values, emails or tokens in logs."""

import logging
import re

_PATTERNS = [
    (re.compile(r"[\w.+\-]+@[\w\-]+(?:\.[\w\-]+)+"), "[email]"),
    (re.compile(r"(?<!\w)\+?\d[\d\s().\-]{6,}\d"), "[number]"),
    (re.compile(r"\b[A-Za-z0-9_\-]{32,}\b"), "[token]"),
]


def scrub(text):
    for rx, rep in _PATTERNS:
        text = rx.sub(rep, text)
    return text


class ScrubFilter(logging.Filter):
    def filter(self, record):
        try:
            message = record.getMessage()
        except Exception:
            return True
        record.msg, record.args = scrub(message), ()
        return True
