from django.http import HttpResponse
from ..models import *
import json
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def add_transport(request):
    request_body = json.loads(request.body)
    number_plate = request_body["number_plate"]
    type = request_body["type"]
    group_id = request_body["group_id"]


    try:
        group = Group.objects.get(id = group_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This group is not exist"}),
            content_type="application/json",
            status=200,
        )
    

    transport = Transport(number_plate = number_plate,type = type , group = group)
    transport.save()

    return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )


@require_http_methods(["POST"])
def get_transports(request):
    request_body = json.loads(request.body)
    group_id = request_body["group_id"]

    try:
        group = Group.objects.get(id = group_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This group is not exist"}),
            content_type="application/json",
            status=200,
        )
    
    transports = Transport.objects.filter(group = group).values()
    transports = list(transports)

    for transport in transports:
        transport["id"] = str(transport["id"])
        transport["group_id"] = str(transport["group_id"])

    return HttpResponse(
        content=json.dumps({"transports": transports}),
        content_type="application/json",
        status=200,
    )


@require_http_methods(["POST"])
def delete_transport(request):
    request_body = json.loads(request.body)
    transport_id = request_body["transport_id"]

    try:
        transport = Transport.objects.get(id = transport_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This transport is not exist"}),
            content_type="application/json",
            status=200,
        )
    
    transport.delete()

    return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )
    