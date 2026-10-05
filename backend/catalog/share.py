"""One registry drives every share control on every page (rule R25, plan appendix C.1). Add a channel here and it
appears everywhere, except where its hide rule says otherwise."""

from urllib.parse import quote

CHANNELS = [
    {"id": "native", "label_key": "share", "group": "main", "kind": "native"},
    {
        "id": "whatsapp",
        "label": "WhatsApp",
        "group": "main",
        "kind": "link",
        "url": lambda c: "https://wa.me/?text=" + c["text"],
    },
    {"id": "copy", "label_key": "copy_link", "group": "main", "kind": "copy"},
    {
        "id": "facebook",
        "label": "Facebook",
        "group": "more",
        "kind": "link",
        "url": lambda c: "https://www.facebook.com/sharer/sharer.php?u=" + c["url"],
    },
    {
        "id": "email",
        "label": "Email",
        "group": "more",
        "kind": "link",
        "url": lambda c: "mailto:?subject=" + quote(c["title"]) + "&body=" + c["text"],
    },
    {
        "id": "linkedin",
        "label": "LinkedIn",
        "group": "more",
        "kind": "link",
        "url": lambda c: "https://www.linkedin.com/sharing/share-offsite/?url=" + c["url"],
    },
    {
        "id": "x",
        "label": "X",
        "group": "more",
        "kind": "link",
        "url": lambda c: "https://x.com/intent/tweet?text=" + quote(c["title"]) + "&url=" + c["url"],
    },
]


def tracked(url, channel, campaign):
    return f"{url}{'&' if '?' in url else '?'}utm_source={channel}&utm_medium=share&utm_campaign={campaign}"


def build(title, line, url, campaign, hidden=False):
    """Return the channels to render. `hidden` removes every share control (individuals, child-facing, do_not_share)."""
    if hidden:
        return []
    out = []
    for ch in CHANNELS:
        link = tracked(url, ch["id"], campaign)
        ctx = {"title": title, "url": quote(link, safe=""), "text": quote(f"{title}. {line} {link}")}
        out.append(
            {
                "id": ch["id"],
                "label": ch.get("label"),
                "label_key": ch.get("label_key"),
                "group": ch["group"],
                "kind": ch["kind"],
                "href": ch["url"](ctx) if "url" in ch else "",
                "copy": url,
                "title": title,
            }
        )
    return out
