from django.http import HttpResponse
from ..models import *
import json
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def get_rooms(request):
    rooms = Room.objects.all().values()

    rooms = Room.objects.all().values()
    rooms = list(rooms)
    for room in rooms:
        room["id"] = str(room["id"])
        room["group_id"] = str(room["group_id"])

    return HttpResponse(
        content=json.dumps({"rooms": rooms}),
        content_type="application/json",
        status=200,
    )


@require_http_methods(["POST"])
def get_own_room(request):
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
    
    room = {
        "id": str(group.room.id),
        "name": str(group.room.name),
        "area": str(group.room.area),
        "price": str(group.room.price),
        "description": str(group.room.description),
    } if group.room else "null"

    return HttpResponse(
        content=json.dumps({"room": room}),
        content_type="application/json",
        status=200,
    )
