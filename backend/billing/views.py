from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST

from accounts.roles import has_cap
from entries.models import Entry
from places.models import Place
from taxonomy.models import Concept

from . import services
from .models import Order, Product

LOGIN = "/account/login/"


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def subscription_page(request):
    errors = []
    if request.method == "POST":
        product = Product.objects.filter(key=request.POST.get("product"), active=True).first()
        place = Place.objects.filter(path=request.POST.get("scope", ""), status="active").first()
        concept = Concept.objects.filter(kind="list_type", slug=request.POST.get("type", "")).first()
        entry = Entry.objects.filter(uid=request.POST.get("entry", "")).first() if request.POST.get("entry") else None
        if product is None:
            errors.append(("product", "Choose a product."))
        else:
            try:
                order = services.create_order(
                    request.user, product, scope_path=place.path if place else "", concept=concept, entry=entry
                )
            except services.BillingError as exc:
                errors.append(("product", str(exc)))
            else:
                return redirect(f"/account/orders/{order.ref}/")
    return render(
        request,
        "billing/subscription.html",
        {
            "products": Product.objects.filter(active=True),
            "orders": Order.objects.filter(buyer=request.user).order_by("-id")[:20],
            "places": Place.objects.filter(status="active").exclude(level="world").order_by("path")[:300],
            "types": Concept.objects.filter(kind="list_type").order_by("slug"),
            "errors": errors,
            "robots": "noindex,nofollow",
            "title": "Plans",
        },
    )


@login_required(login_url=LOGIN)
def order_page(request, ref):
    order = Order.objects.filter(ref=ref, buyer=request.user).select_related("product").first()
    if order is None:
        return HttpResponse(status=404)
    from django.conf import settings

    return render(
        request,
        "billing/order.html",
        {
            "order": order,
            "instructions": getattr(settings, "PAYMENT_INSTRUCTIONS", ""),
            "robots": "noindex,nofollow",
            "title": "Order",
        },
    )


@csrf_exempt
@require_POST
def webhook(request, provider):
    status, msg = services.handle_webhook(provider, request.body, request.headers.get("X-Signature", ""))
    return HttpResponse(msg, status=status, content_type="text/plain")


def staff_orders(request):
    if not has_cap(request.user, "record_payment"):
        return HttpResponseForbidden("Not allowed")
    if request.method == "POST":
        order = Order.objects.filter(ref=request.POST.get("order", "")).first()
        try:
            if order is None:
                raise services.BillingError("unknown order")
            amount = int(request.POST.get("amount_minor", "0"))
            services.record_payment(
                order,
                provider="manual",
                provider_ref=request.POST.get("reference", "").strip() or f"manual-{order.ref}",
                amount_minor=amount,
                fees_minor=int(request.POST.get("fees_minor", "0") or 0),
                actor=request.user,
            )
            messages.success(request, f"Payment recorded for {order.ref}")
        except (services.BillingError, ValueError) as exc:
            messages.error(request, str(exc))
        return redirect("/staff/orders/")
    return render(
        request,
        "billing/staff_orders.html",
        {
            "orders": Order.objects.filter(state="pending")
            .select_related("buyer", "product")
            .order_by("created_at")[:100],
            "robots": "noindex,nofollow",
            "title": "Orders",
        },
    )
