from django.db import models
import uuid



class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30,default='')
    password = models.CharField(max_length=30,default='')
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    role = models.CharField(max_length=20,default='')



class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=30,default='')
    number_of_members = models.IntegerField(default=0)
    donate = models.FloatField(default=0)



class Personal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    citizen_identification_card = models.CharField(max_length=30,default='')
    avatar = models.CharField(max_length=100,default='')
    name = models.CharField(max_length=30,default='')
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20,default='')
    email = models.CharField(max_length=30,default='')
    group = models.ForeignKey(Group,on_delete=models.CASCADE)



class Transport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number_plate = models.CharField(max_length=30,default='')
    type = models.CharField(max_length=30,default='')
    group = models.ForeignKey(Group,on_delete=models.CASCADE)



class Register(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    room = models.ForeignKey('Room',on_delete=models.CASCADE)
    request = models.CharField(max_length=30,default='')



class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30,default='')
    area = models.FloatField(default=0)
    price = models.FloatField(default=0)
    description = models.CharField(max_length=200,default='')
    electric_bill = models.FloatField(default=0)
    water_bill = models.FloatField(default=0)
    group = models.OneToOneField(Group,on_delete=models.SET_NULL,null=True)