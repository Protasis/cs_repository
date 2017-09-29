from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
import os
from bleach import clean
from markdown import markdown
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.utils.safestring import mark_safe
from .models import Paper, Project, WhitePaper, Deliverable
from functools import wraps
# Create your views here.

ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
    'p',
]


def index(request):
    return HttpResponse("Protasis CollabTool")


# we need a decorator to check credentials
def check_group_access(function=None, group_access=None, user=None):
    # check: (u.authenticated and u can access) or (anonymous in access)
    # from IPython import embed
    # embed()
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and any(len(u.groups.filter(id=g.id)) for g in group_access.filter(read=True)))
    if function:
        return actual_decorator(function)
    return actual_decorator


def project(request, p):
        template = loader.get_template('project.html')
        context = {
            'project_slug': p.slug,
            'project': p,
            'description': mark_safe(clean(markdown(p.description), ALLOWED_TAGS))
        }

        return HttpResponse(template.render(context, request))


def paper(request, p):
    template = loader.get_template('paper.html')
    context = {
        'paper_slug': p.slug,
        'paper': p,
    }

    return HttpResponse(template.render(context, request))


def get_and_check(request, cl, id, slug):

    _classes = {
        'paper': [Paper, paper],
        'project': [Project, project],
        'whitepaper': [WhitePaper, paper],
        'deliverable': [Deliverable, paper],
    }

    if cl not in _classes:
        return HttpResponseNotFound()
    _opts = _classes[cl]
    p = get_object_or_404(_opts[0], pk=id)

    _view = check_group_access(_opts[1], p.group_access)

    print _view
    return _view(request, p)


# TODO: update to new group access policy!
def protected_data(request, paper_id,):
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
    return serve_static(request, path)


def serve_static(request, path):
    file_root = settings.DATA_ROOT
    # set PRIVATE_MEDIA_USE_XSENDFILE in your deployment-specific settings file
    # should be false for development, true when your webserver supports xsendfile
    if settings.PRIVATE_MEDIA_USE_XSENDFILE:
        name = os.path.join(file_root, path)
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
