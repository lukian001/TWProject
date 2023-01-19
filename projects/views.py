import json

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from .models import Project, Instance
import random
import string
from django.views.decorators.csrf import csrf_exempt
from io import StringIO
from contextlib import redirect_stdout


def generate_new_name():
    return ''.join(random.choices(string.ascii_lowercase, k=10))


def project(request):
    if request.user.is_authenticated:
        project_name = request.POST.get("project_name")
        new_project = Project()
        new_project.name = project_name
        new_project.owner = request.user
        new_project.save()
        new_instance = Instance()
        new_instance.name = "main"
        new_instance.project = new_project
        new_instance.save()

        return HttpResponse(new_project.name)


def details_project(request, slug):
    project = Project.objects.get(name=slug)
    return render(request, 'coding.html', {'project': project})


@csrf_exempt
def run_code(request, slug):
    if request.method == "POST":
        code = request.POST.get('code', None)
        f = StringIO()
        try:
            with redirect_stdout(f):
                exec(code)
            output = f.getvalue()
        except:
            output = "Exceptie!"

        return JsonResponse({'output': output})


@csrf_exempt
def new_instance(request, slug):
    if request.user.is_authenticated:
        file_name = request.POST.get('new_file_name', None)
        project = Project.objects.get(name=slug)
        instance = Instance()
        instance.name = file_name
        instance.project = project
        instance.save()
        template = render_to_string('file_element.html', {'instance': instance,
                                                          })

        return JsonResponse(template, safe=False)


def get_instance_code(request, slug):
    if request.user.is_authenticated:
        instance_name = request.POST.get('instance_name', None)
        curr_project = Project.objects.get(name=slug)
        instance = Instance.objects.get(name=instance_name, project=curr_project)

        return HttpResponse(instance.code)


def save_instance_code(request, slug):
    if request.user.is_authenticated:
        instance_name = request.POST.get('instance_name', None)
        instance_code = request.POST.get('instance_code', None)
        curr_project = Project.objects.get(name=slug)
        instance = Instance.objects.get(name=instance_name, project=curr_project)
        instance.code = instance_code
        instance.save()

        return HttpResponse("Saved")
