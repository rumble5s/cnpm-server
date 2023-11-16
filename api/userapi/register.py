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
        group = Group.objects.get(id = group_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This group is not exist"}),
            content_type="application/json",
            status=200,
        )
    
    try:
        room = Room.objects.get(id = room_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This room is not exist"}),
            content_type="application/json",
            status=200,
        )
    
    try:
        register = Register.objects.get(group = group , room = room)
        return HttpResponse(
            content=json.dumps({"error": "This register is exist"}),
            content_type="application/json",
            status=200,
        )
    except:
        if request == "unhire" and room.group != group :
            return HttpResponse(
                content=json.dumps({"error": "This register is invalid"}),
                content_type="application/json",
                status=200,
            )
        register = Register(group = group , room = room , request = request)
        register.save()
        return HttpResponse(
                content=json.dumps("Successful"),
                content_type="application/json",
                status=200,
            )
