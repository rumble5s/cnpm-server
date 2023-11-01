from django.http import HttpResponse
from ..models import *
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def SignUp(request):
    request_body = json.loads(request.body)
    username = request_body["username"]
    password = request_body["password"]
    type = request_body["type"]

    try:
        account = Account.objects.get(username = username)
        return HttpResponse(
            content=json.dumps({"error": "This username is exist"}),
            content_type="application/json",
            status=200,
        )
    
    except ObjectDoesNotExist :
        group = Group(name = username , type = type)
        group.save()
        account = Account(username = username , password = password , role = "user" , group = group)
        account.save()
        return HttpResponse(
            content=json.dumps({"group_id": str(group.id),"isadmin":False}),
            content_type="application/json",
            status=200,
        )

@require_http_methods(["POST"])
def SignIn(request):
    request_body = json.loads(request.body)
    username = request_body["username"]
    password = request_body["password"]

    try:
        account = Account.objects.get(username = username , password = password)

        if account.role == 'admin' :
            return HttpResponse(
            content=json.dumps({"group_id": 'admin',"isadmin":str(account.id)}),
            content_type="application/json",
            status=200,
            )

        group = account.group

        return HttpResponse(
            content=json.dumps({"group_id": str(group.id),"isadmin":False}),
            content_type="application/json",
            status=200,
        )
    
    except ObjectDoesNotExist :
        return HttpResponse(
            content=json.dumps({"error": "Wrong answer or password"}),
            content_type="application/json",
            status=200,
        )