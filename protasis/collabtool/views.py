from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from .models import Project
# Create your views here.


def index(request):
    return HttpResponse("Hello world")


def project(request, project_id, project_slug):
    template = loader.get_template('project.html')

    project = get_object_or_404(Project, pk=project_id)

    context = {
        'project_slug': project_slug,
        'project': project,
    }

    return HttpResponse(template.render(context, request))
