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
