from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import campaigns


@csrf_exempt
@require_POST
def messaging_webhook(request, provider):
    status, msg = campaigns.handle_callback(provider, request.body, request.headers.get("X-Signature", ""))
    return HttpResponse(msg, status=status, content_type="text/plain")
