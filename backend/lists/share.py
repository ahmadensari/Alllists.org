"""One registry drives every share control on every page. Add a channel here and it appears everywhere."""
from urllib.parse import quote

CHANNELS = [
    {"id": "whatsapp", "label": "WhatsApp", "group": "main", "kind": "link",
     "url": lambda c: "https://wa.me/?text=" + c["text"]},
    {"id": "copy", "label": "Copy link", "group": "main", "kind": "copy"},
    {"id": "facebook", "label": "Facebook", "group": "more", "kind": "link",
     "url": lambda c: "https://www.facebook.com/sharer/sharer.php?u=" + c["url"]},
    {"id": "email", "label": "Email", "group": "more", "kind": "link",
     "url": lambda c: "mailto:?subject=" + quote(c["title"]) + "&body=" + c["text"]},
    {"id": "linkedin", "label": "LinkedIn", "group": "more", "kind": "link",
     "url": lambda c: "https://www.linkedin.com/sharing/share-offsite/?url=" + c["url"]},
    {"id": "x", "label": "X", "group": "more", "kind": "link",
     "url": lambda c: "https://x.com/intent/tweet?text=" + quote(c["title"]) + "&url=" + c["url"]},
]


def utm(url, channel, campaign):
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source={channel}&utm_medium=share&utm_campaign={campaign}"


def build(title, line, url, campaign, hide=()):
    out = []
    for ch in CHANNELS:
        if ch["id"] in hide:
            continue
        tracked = utm(url, ch["id"], campaign)
        ctx = {"title": title, "url": quote(tracked, safe=""), "text": quote(f"{title}. {line} {tracked}")}
        out.append({"id": ch["id"], "label": ch["label"], "group": ch["group"], "kind": ch["kind"],
                    "href": ch["url"](ctx) if "url" in ch else "", "copy": tracked})
    return out
