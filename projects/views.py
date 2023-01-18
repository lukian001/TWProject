from django.shortcuts import render
from django.http import JsonResponse
from .models import Project
import random
import string
from django.views.decorators.csrf import csrf_exempt
from io import StringIO
from contextlib import redirect_stdout


def generate_new_name():
    return ''.join(random.choices(string.ascii_lowercase, k=10))


def project(request):
    new_project = Project()
    new_project.name = generate_new_name()
    new_project.owner = request.user
    new_project.save()
    return render(request, 'coding.html')


def details_project(request, slug):
    project = Project.objects.get(name=slug)
    return render(request, 'coding.html', {'project': project})


@csrf_exempt
def run_code(request):
    if request.method == "POST":
        code = request.POST.get('TextEntered', None)
        f = StringIO()
        try:
            with redirect_stdout(f):
                exec(code)
            output = f.getvalue()
        except:
            output = "Exceptie!"

        return JsonResponse({'output': output})
