from django.http import HttpResponse
from ..models import *
import json
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def admin_get_groups(request):
    request_body = json.loads(request.body)
    auth = request_body["auth"]

    try:
        admin = Account.objects.get(id=auth)
    except:
        return HttpResponse(
            content=json.dumps({"error": "Invalid auth"}),
            content_type="application/json",
            status=200,
        )

    if admin.role != "admin":
        return HttpResponse(
            content=json.dumps({"error": "You are not an admin"}),
            content_type="application/json",
            status=200,
        )

    groups = Group.objects.all().values()
    groups = list(groups)
    for group in groups:
        group["id"] = str(group["id"])

    return HttpResponse(
        content=json.dumps({"groups": groups}),
        content_type="application/json",
        status=200,
    )
