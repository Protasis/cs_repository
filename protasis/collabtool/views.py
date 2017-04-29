from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello world")


def project(request, project_id, project_slug):
    template = loader.get_template('project.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
