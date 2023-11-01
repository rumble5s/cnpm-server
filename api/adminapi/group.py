from django.http import HttpResponse
from ..models import *
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def admin_get_groups(request):
    request_body=json.loads(request.body)
    auth = request_body["auth"]
    
    try:
        admin = Account.objects.get(id=auth)

        if admin.role != "admin" :
            return HttpResponse(
            content=json.dumps({"error":"You are not an admin"}),
            content_type="application/json",
            status=200,
        )

        groups = Group.objects.all().values()
        groups = list(groups)

        return HttpResponse(
            content=json.dumps({"groups":str(groups)}),
            content_type="application/json",
            status=200,
        )

    except:
        return HttpResponse(
            content=json.dumps({"error":"Invalid auth"}),
            content_type="application/json",
            status=200,
        )


@require_http_methods(["POST"])
def admin_edit_groups(request):
    request_body=json.loads(request.body)
    auth = request_body["auth"]
    group_id = request_body["group_id"]
    name = request_body["name"]
    type  = request_body["type"]
    donate = request_body["donate"]
    
    try:
        admin = Account.objects.get(id=auth)

        if admin.role != "admin" :
            return HttpResponse(
            content=json.dumps({"error":"You are not admin"}),
            content_type="application/json",
            status=200,
        )

        try:
            group = Group.objects.get(id=group_id)
            group.name = name
            group.type = type
            group.donate = donate
            group.save()
            return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )
        except:
            return HttpResponse(
            content=json.dumps({"error":"This group is not exist"}),
            content_type="application/json",
            status=200,
        )

    except:
        return HttpResponse(
            content=json.dumps({"error":"Invalid auth"}),
            content_type="application/json",
            status=200,
        )