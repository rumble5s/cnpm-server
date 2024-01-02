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

    registers = Register.objects.all()
    res_registers = []

    for register in registers:
        res_registers.append(
            {
                "id": str(register.id),
                "request": str(register.request),
                "status": str(register.status),
                "group": {
                    "id": str(register.group.id),
                    "name": str(register.group.name),
                    "type": str(register.group.type),
                },
                "room": {
                    "id": str(register.room.id),
                    "name": str(register.room.name),
                    "area": str(register.room.area),
                    "price": str(register.room.price),
                    "description": str(register.room.description),
                },
            }
        )

    return HttpResponse(
        content=json.dumps({"registers": res_registers}),
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
        register = Register.objects.get(id=register_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This register is not exist"}),
            content_type="application/json",
            status=200,
        )

    if register.status != "pending":
        return HttpResponse(
            content=json.dumps({"error": "This register is not pending"}),
            content_type="application/json",
            status=200,
        )

    group = register.group
    room = register.room

    if register.request == "hire":
        try:
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

    if register.request == "unhire":
        room.group = None

    register.status = "Accepted"
    register.save()

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
        register = Register.objects.get(id=register_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This register is not exist"}),
            content_type="application/json",
            status=200,
        )

    if register.status != "pending":
        return HttpResponse(
            content=json.dumps({"error": "This register is not pending"}),
            content_type="application/json",
            status=200,
        )

    register.status = "Denied"
    register.save()
    
    return HttpResponse(
        content=json.dumps("Successful"),
        content_type="application/json",
        status=200,
    )
