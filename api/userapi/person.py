from django.http import HttpResponse
from ..models import *
import json
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def add_person(request):
    citizen_identification_card = request.POST.get("citizen_identification_card")
    avatar = request.FILES.get("avatar")
    name = request.POST.get("name")
    date_of_birth = request.POST.get("date_of_birth")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    group_id = request.POST.get("group_id")

    try:
        group = Group.objects.get(id=group_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This group is not exist"}),
            content_type="application/json",
            status=200,
        )

    person = Person(
        citizen_identification_card=citizen_identification_card,
        avatar=avatar,
        name=name,
        date_of_birth=date_of_birth,
        phone=phone,
        email=email,
        group=group,
    )

    person.save()

    return HttpResponse(
        content=json.dumps("Successful"),
        content_type="application/json",
        status=200,
    )


@require_http_methods(["POST"])
def get_persons(request):
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

    persons = Person.objects.filter(group=group).values()
    persons = list(persons)

    for person in persons:
        person["id"] = str(person["id"])
        person["group_id"] = str(person["group_id"])
        person["date_of_birth"] = person["date_of_birth"].isoformat()

    return HttpResponse(
        content=json.dumps({"persons": persons}),
        content_type="application/json",
        status=200,
    )


@require_http_methods(["POST"])
def edit_person(request):
    person_id = request.POST.get("person_id")
    citizen_identification_card = request.POST.get("citizen_identification_card")
    avatar = request.FILES.get("avatar")
    name = request.POST.get("name")
    date_of_birth = request.POST.get("date_of_birth")
    phone = request.POST.get("phone")
    email = request.POST.get("email")

    try:
        person = Person.objects.get(id=person_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This person is not exist"}),
            content_type="application/json",
            status=200,
        )

    person.citizen_identification_card = citizen_identification_card
    person.avatar = avatar
    person.name = name
    person.date_of_birth = date_of_birth
    person.phone = phone
    person.email = email

    person.save()

    return HttpResponse(
        content=json.dumps("Successful"),
        content_type="application/json",
        status=200,
    )


@require_http_methods(["POST"])
def delete_person(request):
    request_body = json.loads(request.body)
    person_id = request_body["person_id"]

    try:
        person = Person.objects.get(id=person_id)
    except:
        return HttpResponse(
            content=json.dumps({"error": "This person is not exist"}),
            content_type="application/json",
            status=200,
        )

    person.delete()

    return HttpResponse(
        content=json.dumps("Successful"),
        content_type="application/json",
        status=200,
    )
