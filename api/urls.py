from .loginapi.login import *
from .adminapi.group import *
from django.urls import path

urlpatterns = [
    path('signup/',SignUp),
    path('signin/',SignIn),
    path('admin_get_groups/',admin_get_groups),
    path('admin_edit_groups/',admin_edit_groups)
]