from django.http import HttpResponse
from ..models import *
import json
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def admin_show_registers(request):
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
    
    registers = Register.objects.all().values()
    registers = list(registers)
    for register in registers:
        register["id"] = str(register["id"])
        register["group_id"] = str(register["group_id"])
        register["room_id"] = str(register["room_id"])

    return HttpResponse(
            content=json.dumps({"registers": registers}),
            content_type="application/json",
            status=200,
        )


@require_http_methods(["POST"])
def admin_accept_register(request):
    request_body = json.loads(request.body)
    auth = request_body["auth"]
    register_id = request_body["register_id"]

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
    
    try:
        register = Register.objects.get(id = register_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This register is not exist"}),
            content_type="application/json",
            status=200,
        )
    
    if register.status != "pending" :
        return HttpResponse(
            content=json.dumps({"error": "This register is not pending"}),
            content_type="application/json",
            status=200,
        )
    
    group = register.group
    room = register.room

    if register.request == "hire" :
        try :
            group.room
            return HttpResponse(
                content=json.dumps({"error": "This group was hired a room"}),
                content_type="application/json",
                status=200,
            )
        except:
            if room.group == None:
                room.group = group
                room.save()
            else:
                return HttpResponse(
                    content=json.dumps({"error": "This room has been hired"}),
                    content_type="application/json",
                    status=200,
                )
    

    if register.request == "unhire" :
        room.group = None
        room.save()

    register.status = "Accepted"
    
    return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )
    

@require_http_methods(["POST"])
def admin_deny_register(request):
    request_body = json.loads(request.body)
    auth = request_body["auth"]
    register_id = request_body["register_id"]


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
    
    try:
        register = Register.objects.get(id = register_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This register is not exist"}),
            content_type="application/json",
            status=200,
        )
    
    if register.status != "pending" :
        return HttpResponse(
            content=json.dumps({"error": "This register is not pending"}),
            content_type="application/json",
            status=200,
        )
    
    register.status = "Denied"
    
    return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )