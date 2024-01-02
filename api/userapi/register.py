from django.http import HttpResponse
from ..models import *
import json
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def make_a_register(request):
    request_body = json.loads(request.body)
    group_id = request_body["group_id"]
    room_id = request_body["room_id"]
    request = request_body["request"]

    try:
        group = Group.objects.get(id=group_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This group is not exist"}),
            content_type="application/json",
            status=200,
        )

    try:
        room = Room.objects.get(id=room_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This room is not exist"}),
            content_type="application/json",
            status=200,
        )

    try:
        register = Register.objects.get(group=group, room=room, status="pending")
        return HttpResponse(
            content=json.dumps({"error": "This register is exist"}),
            content_type="application/json",
            status=200,
        )
    except:
        if request == "unhire" and room.group != group:
            return HttpResponse(
                content=json.dumps({"error": "This register is invalid"}),
                content_type="application/json",
                status=200,
            )
        register = Register(group=group, room=room, request=request, status="pending")
        register.save()
        return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )


@require_http_methods(["POST"])
def get_registers(request):
    request_body = json.loads(request.body)
    group_id = request_body["group_id"]

    try:
        group = Group.objects.get(id=group_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This group is not exist"}),
            content_type="application/json",
            status=200,
        )

    registers = Register.objects.filter(group=group)
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
def delete_register(request):
    request_body = json.loads(request.body)
    register_id = request_body["register_id"]

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

    register.delete()

    return HttpResponse(
        content=json.dumps("Successful"),
        content_type="application/json",
        status=200,
    )
