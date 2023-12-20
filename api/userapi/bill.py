from django.http import HttpResponse
from ..models import *
import json, datetime
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def get_bills(request):
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

    bills = Bill.objects.filter(group_id=group_id)
    res_bills = []

    for bill in bills:
        res_bills.append(
            {
                "id": str(bill.id),
                "title": str(bill.title),
                "create_at": str(bill.create_at),
                "group": {
                    "id": str(bill.group.id),
                    "name": str(bill.group.name),
                    "type": str(bill.group.type),
                },
                "room": {
                    "id": str(bill.room.id),
                    "name": str(bill.room.name),
                    "area": str(bill.room.area),
                    "price": str(bill.room.price),
                    "description": str(bill.room.description),
                },
                "room_bill": str(bill.room_bill),
                "electric_bill": str(bill.electric_bill),
                "water_bill": str(bill.water_bill),
                "donate": str(bill.donate),
                "paid": str(bill.paid),
            }
        )

    return HttpResponse(
        content=json.dumps({"bills": res_bills}),
        content_type="application/json",
        status=200,
    )
