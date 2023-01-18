from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('create-group/', views.create_group, name="create_group"),
    path('<group_name>', views.group_page, name="group_page"),
    path('<group_name>/enter_group/', views.enter_group, name="enter_group"),
    path('<group_name>/leave_group/', views.leave_group, name="leave_group"),
    path('<group_name>/delete_group/', views.delete_group, name="delete_group"),
    path('<group_name>/change_group_data/', views.change_group, name="change_group"),
    path('<group_name>/members/', views.group_members, name="group_members"),
]
