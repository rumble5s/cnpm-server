from .loginapi.login import *

from .adminapi.group import *
from .adminapi.room import *
from .adminapi.register import *
from .adminapi.bill import *

from .userapi.person import *
from .userapi.register import *
from .userapi.transport import *
from .userapi.room import *
from .userapi.bill import *

from django.urls import path

urlpatterns = [
    # Login
    path('signup/',SignUp),
    path('signin/',SignIn),
    
    # Admin api
    path('admin_get_groups/',admin_get_groups),

    path('admin_get_rooms/',admin_get_rooms),
    path('admin_create_room/',admin_create_room),
    path('admin_edit_room/',admin_edit_room),
    path('admin_delete_room/',admin_delete_room),

    path('admin_show_registers/',admin_show_registers),
    path('admin_accept_register/',admin_accept_register),
    path('admin_deny_register/',admin_deny_register),

    path('admin_get_bills/',admin_get_bills),
    path('admin_create_bill/',admin_create_bill),
    path('admin_delete_bill/',admin_delete_bill),
    path('admin_accept_bill/',admin_accept_bill),

    # User api
    path('add_person/',add_person),
    path('get_persons/',get_persons),
    path('edit_person/',edit_person),
    path('delete_person/',delete_person),

    path('make_a_register/',make_a_register),
    path('get_registers/',get_registers),
    path('delete_register/',delete_register),

    path('add_transport/',add_transport),
    path('get_transports/',get_transports),
    path('delete_transport/',delete_transport),

    path('get_rooms/',get_rooms),
    path('get_own_room/',get_own_room),

    path('get_bills/',get_bills)
]