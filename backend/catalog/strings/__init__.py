"""Interface text in English and Urdu (plan 8.5). Whole sentences with placeholders, plural forms per key.

The environment has no gettext tools, so catalogues are Python modules for now; moving them to .po files later is
mechanical because every entry is a whole sentence. English is the source language; a missing Urdu entry falls
back to English and is reported by `missing_translations()`."""

import re

from .en import EN
from .ur import UR

LANGUAGES = ("en", "ur")
_PLACEHOLDER = re.compile(r"\{(\w+)\}")


def _entry(lang, key):
    table = EN if lang == "en" else UR
    return table[key] if key in table else EN[key]


def t(lang, key, **kw):
    """Translate a key. Plural entries are dicts {"one": ..., "other": ...} chosen by kw["n"]."""
    value = _entry(lang, key)
    if isinstance(value, dict):
        n = kw.get("n", 0)
        value = value["one"] if n == 1 and "one" in value else value["other"]
    return value.format(**kw) if kw or "{" in value else value


def placeholders(value):
    if isinstance(value, dict):
        out = set()
        for v in value.values():
            out |= set(_PLACEHOLDER.findall(v))
        return out
    return set(_PLACEHOLDER.findall(value))


def missing_translations():
    return sorted(set(EN) - set(UR))


def placeholder_mismatches():
    return sorted(k for k in UR if k in EN and placeholders(UR[k]) != placeholders(EN[k]))


class Translator:
    """Bound to a language; used in templates as `T.key` or `T.n_entries(n=5)` through the `tr` tag."""

    def __init__(self, lang):
        self.lang = lang

    def __call__(self, key, **kw):
        return t(self.lang, key, **kw)
