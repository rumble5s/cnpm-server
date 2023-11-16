from .loginapi.login import *

from .adminapi.group import *
from .adminapi.room import *
from .adminapi.register import *

from .userapi.register import *
from django.urls import path

urlpatterns = [
    path('signup/',SignUp),
    path('signin/',SignIn),

    path('admin_get_groups/',admin_get_groups),
    path('admin_edit_group/',admin_edit_group),
    path('admin_get_rooms/',admin_get_rooms),
    path('admin_create_room/',admin_create_room),
    path('admin_edit_room/',admin_edit_room),
    path('admin_delete_room/',admin_delete_room),
    path('admin_show_registers/',admin_show_registers),
    path('admin_accept_register/',admin_accept_register),

    path('make_a_register/',make_a_register),
]