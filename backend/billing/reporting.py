"""Revenue reporting by month, currency and product kind (plan 12.4, P5.06). Each currency is reported on its own;
a consolidated line appears only when rates are configured, and is marked indicative."""

import csv
import io
from collections import defaultdict
from decimal import Decimal

from django.conf import settings
from ledger.models import Sale


def revenue_report(year=None):
    """Rows: {month, currency, kind, sales, gross, fees, tax, net, contributors, platform, refunded_gross}."""
    live = Sale.objects.filter(state="recorded")
    if year:
        live = live.filter(ts__year=year)
    out = defaultdict(
        lambda: dict(sales=0, gross=0, fees=0, tax=0, net=0, contributors=0, platform=0, refunded_gross=0)
    )
    for s in live:
        key = (s.ts.strftime("%Y-%m"), s.currency, s.kind)
        row = out[key]
        paid = sum(a.amount_minor for a in s.allocations.all() if a.reversed_at is None)
        row["sales"] += 1
        row["gross"] += s.gross_minor
        row["fees"] += s.fees_minor
        row["tax"] += s.tax_minor
        row["net"] += s.net_minor
        row["contributors"] += paid
        row["platform"] += s.net_minor - paid
    refunded = Sale.objects.filter(state="refunded")
    if year:
        refunded = refunded.filter(ts__year=year)
    for s in refunded:
        out[(s.ts.strftime("%Y-%m"), s.currency, s.kind)]["refunded_gross"] += s.gross_minor
    return [dict(month=k[0], currency=k[1], kind=k[2], **v) for k, v in sorted(out.items())]


def consolidated_usd(rows):
    """Indicative total in USD minor units from configured rates; None when a currency has no rate."""
    rates = getattr(settings, "REPORT_RATES_TO_USD", {})
    total = Decimal(0)
    for r in rows:
        if r["currency"] == "USD":
            total += r["gross"]
        elif r["currency"] in rates:
            total += Decimal(r["gross"]) * Decimal(str(rates[r["currency"]]))
        else:
            return None
    return int(total)


def revenue_csv(rows):
    out = io.StringIO()
    cols = [
        "month",
        "currency",
        "kind",
        "sales",
        "gross",
        "fees",
        "tax",
        "net",
        "contributors",
        "platform",
        "refunded_gross",
    ]
    w = csv.DictWriter(out, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
    return out.getvalue()
