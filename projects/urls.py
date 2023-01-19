from django.contrib import admin
from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.project, name='project'),
    path('<slug>/', views.details_project, name='det_project'),
    path('<slug>/runcode/', views.run_code, name='run_code'),
    path('<slug>/create_file/', views.new_instance, name="create_file"),
    path('<slug>/instance_code/', views.get_instance_code, name="instance_code"),
    path('<slug>/save_code/', views.save_instance_code, name="save_code")
]