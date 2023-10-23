from .login import *
from django.urls import path

urlpatterns = [
    path('signup/',SignUp),
    path('signin/',SignIn)
]