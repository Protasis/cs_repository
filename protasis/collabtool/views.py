from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os
from django.http import Http404
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


@login_required
def protected_data(request, path, file_root=None):
    # set PRIVATE_MEDIA_ROOT to the root folder of your private media files
    name = os.path.join(file_root, path)
    if not os.path.isfile(name):
        raise Http404("File not found.")

    # set PRIVATE_MEDIA_USE_XSENDFILE in your deployment-specific settings file
    # should be false for development, true when your webserver supports xsendfile
    if settings.PRIVATE_MEDIA_USE_XSENDFILE:
        response = HttpResponse()
        response['X-Accel-Redirect'] = name  # Nginx
        response['X-Sendfile'] = name  # Apache 2 with mod-xsendfile
        del response['Content-Type']  # let webserver regenerate this
        return response
    else:
        # fallback method
        from django.views.static import serve
        return serve(request, path, file_root)
