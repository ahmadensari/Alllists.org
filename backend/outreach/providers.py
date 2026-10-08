"""Messaging provider adapters (plan 13.2). Only official channels: no unofficial WhatsApp libraries (rule R29).
A concrete provider is chosen after counsel and a bake-off; until then the sandbox provider runs everything."""

import itertools


class SandboxProvider:
    """Records what it was asked to send and returns provider ids. Nothing leaves the machine."""

    name = "sandbox"

    def __init__(self):
        self.sent = []
        self._ids = itertools.count(1)

    def send(self, *, channel, to, body, template_key):
        pid = f"sbx-{next(self._ids)}"
        self.sent.append({"id": pid, "channel": channel, "to": to, "body": body, "template": template_key})
        return pid


PROVIDERS = {"sandbox": SandboxProvider}


def get_provider(name="sandbox"):
    return PROVIDERS[name]()
