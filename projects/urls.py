from django.contrib import admin
from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.project, name='project'),
    path('<slug>/', views.details_project, name='det_project'),
    path('runcode/', views.run_code, name='run_code'),
]