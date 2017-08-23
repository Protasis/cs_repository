from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .models import Paper
# Create your views here.


def index(request):
    return HttpResponse("Protasis CollabTool")


def paper(request, paper_id, paper_slug):
    template = loader.get_template('paper.html')

    paper = get_object_or_404(Paper, pk=paper_id)

    context = {
        'paper_slug': paper_slug,
        'paper': paper,
    }

    return HttpResponse(template.render(context, request))


def protected_data(request, paper_id, file_root=None):
    # set PRIVATE_MEDIA_ROOT to the root folder of your private media files

    paper = get_object_or_404(Paper, pk=paper_id)

    if paper.data_protected:
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        if paper not in request.user.can_access_data.all():
            return HttpResponseForbidden()

    if not (paper.data and paper.data.name):
        return HttpResponseNotFound()

    path = paper.data.name
    return serve_static(request, path, file_root)


def serve_static(request, path, file_root):
    # set PRIVATE_MEDIA_USE_XSENDFILE in your deployment-specific settings file
    # should be false for development, true when your webserver supports xsendfile
    if settings.PRIVATE_MEDIA_USE_XSENDFILE:
        name = os.path.join(settings.DATA_ROOT, path)
        if not os.path.isfile(name):
            return HttpResponseNotFound()
        response = HttpResponse()
        response['X-Accel-Redirect'] = name  # Nginx
        response['X-Sendfile'] = name  # Apache 2 with mod-xsendfile
        del response['Content-Type']  # let webserver regenerate this
        return response
    else:
        # fallback method
        from django.views.static import serve

        path = os.path.join(*os.path.split(path)[1:])
        return serve(request, path, file_root)
