from django.http import HttpResponse
from ..models import *
import json, datetime
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def admin_get_bills(request):
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

    bills = Bill.objects.all()
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


@require_http_methods(["POST"])
def admin_create_bill(request):
    request_body = json.loads(request.body)
    auth = request_body["auth"]
    title = request_body["title"]
    create_at = datetime.date.today()
    room_id = request_body["room_id"]
    electric_bill = request_body["electric_bill"]
    water_bill = request_body["water_bill"]

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
    except:
        return HttpResponse(
            content=json.dumps({"error": "This room is not exist"}),
            content_type="application/json",
            status=200,
        )

    if room.group == None:
        return HttpResponse(
            content=json.dumps({"error": "This room isnt hired"}),
            content_type="application/json",
            status=200,
        )

    bill = Bill(
        title=title,
        create_at=create_at,
        room=room,
        group=room.group,
        room_bill=room.price,
        electric_bill=electric_bill,
        water_bill=water_bill,
    )

    bill.save()

    return HttpResponse(
        content=json.dumps("Successful"),
        content_type="application/json",
        status=200,
    )


@require_http_methods(["POST"])
def admin_delete_bill(request):
    request_body = json.loads(request.body)
    auth = request_body["auth"]
    bill_id = request_body["bill_id"]

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
        bill = Bill.objects.get(id=bill_id)

        if bill.paid == True:
            return HttpResponse(
                content=json.dumps({"error": "This bill has been paid"}),
                content_type="application/json",
                status=200,
            )

        bill.delete()
        return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )
    except:
        return HttpResponse(
            content=json.dumps({"error": "Cant delete this bill"}),
            content_type="application/json",
            status=200,
        )


@require_http_methods(["POST"])
def admin_accept_bill(request):
    request_body = json.loads(request.body)
    auth = request_body["auth"]
    bill_id = request_body["bill_id"]
    donate = request_body["donate"]

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
        bill = Bill.objects.get(id=bill_id)

        if bill.paid == True:
            return HttpResponse(
                content=json.dumps({"error": "This bill has been paid"}),
                content_type="application/json",
                status=200,
            )

        bill.paid = True
        bill.donate = donate
        bill.save()
        return HttpResponse(
            content=json.dumps("Successful"),
            content_type="application/json",
            status=200,
        )
    except:
        return HttpResponse(
            content=json.dumps({"error": "Cant accept this bill"}),
            content_type="application/json",
            status=200,
        )
