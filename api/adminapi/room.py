from django.http import HttpResponse
from ..models import *
import json
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def admin_get_rooms(request):
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

    rooms = Room.objects.all()
    res_rooms = []

    for room in rooms:
        res_rooms.append(
            {
                "id": str(room.id),
                "name": str(room.name),
                "area": str(room.area),
                "price": str(room.price),
                "description": str(room.description),
                "group": {
                    "id": str(room.group.id),
                    "name": str(room.group.name),
                    "type": str(room.group.type),
                }
                if room.group
                else "null",
            }
        )

    return HttpResponse(
        content=json.dumps({"rooms": res_rooms}),
        content_type="application/json",
        status=200,
    )


@require_http_methods(["POST"])
def admin_create_room(request):
    request_body = json.loads(request.body)
    auth = request_body["auth"]
    name = request_body["name"]
    area = request_body["area"]
    price = request_body["price"]
    description = request_body["description"]

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

    room = Room(name=name, area=area, price=price, description=description)
    room.save()
    return HttpResponse(
        content=json.dumps("Successful"),
        content_type="application/json",
        status=200,
    )


@require_http_methods(["POST"])
def admin_edit_room(request):
    request_body = json.loads(request.body)
    auth = request_body["auth"]
    room_id = request_body["room_id"]
    name = request_body["name"]
    area = request_body["area"]
    price = request_body["price"]
    description = request_body["description"]

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
        room = Room.objects.get(id=room_id)
        room.name = name
        room.area = area
        room.price = price
        room.description = description
        room.save()
        return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )
    except:
        return HttpResponse(
            content=json.dumps({"error": "This room is not exist"}),
            content_type="application/json",
            status=200,
        )


@require_http_methods(["POST"])
def admin_delete_room(request):
    request_body = json.loads(request.body)
    auth = request_body["auth"]
    room_id = request_body["room_id"]

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
        room = Room.objects.get(id=room_id)
        room.delete()
        return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )
    except:
        return HttpResponse(
            content=json.dumps({"error": "Cant delete this room"}),
            content_type="application/json",
            status=200,
        )
