# Verbatim read-only copy of backend/core/textfold.py (the repo file is not imported or edited by the benchmarks).
"""Search folding for Urdu, Arabic and Latin text (plan section 7.3).

Unicode normalisation alone does not unify Urdu and Arabic letters: trigram similarity of the same name written with
the two yeh forms was 0.54 before folding. This one function is used for names, place names, concept labels and queries.
"""

import re
import unicodedata

_MAP = {
    0x064A: 0x06CC,
    0x0649: 0x06CC,  # Arabic yeh, alef maksura -> Farsi yeh
    0x0643: 0x06A9,  # Arabic kaf -> keheh
    0x0647: 0x06C1,
    0x06D5: 0x06C1,  # heh, ae -> heh goal
    0x06BE: 0x06C1,  # heh doachashmee -> heh goal
    0x0623: 0x0627,
    0x0625: 0x0627,
    0x0671: 0x0627,
    0x0622: 0x0627,  # alef variants and madda -> alef
    0x06C0: 0x06C1,
    0x0624: 0x0648,  # heh with yeh above, waw with hamza
    0x0626: 0x06CC,  # yeh with hamza
}
_REMOVE = {0x0640, 0x200C, 0x200D, 0x200E, 0x200F, 0x0670}
_DIGITS = {**{0x0660 + i: ord("0") + i for i in range(10)}, **{0x06F0 + i: ord("0") + i for i in range(10)}}
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_SPACE = re.compile(r"\s+")


def fold(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    out = []
    for ch in text:
        cp = ord(ch)
        if cp == 0x200C:  # ZWNJ separates words in Urdu
            out.append(" ")
        elif cp in _REMOVE or 0x064B <= cp <= 0x065F:
            continue
        elif cp in _DIGITS:
            out.append(chr(_DIGITS[cp]))
        elif cp in _MAP:
            out.append(chr(_MAP[cp]))
        else:
            out.append(ch)
    text = "".join(out).lower()
    text = _PUNCT.sub(" ", text)
    return _SPACE.sub(" ", text).strip()
