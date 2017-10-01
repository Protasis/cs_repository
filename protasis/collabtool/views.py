from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os
from bleach import clean
from markdown import markdown
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.utils.safestring import mark_safe
from .models import Paper, Project, WhitePaper, Deliverable, Data
from functools import wraps
# Create your views here.

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.utils import six
from django.utils.decorators import available_attrs
from django.utils.six.moves.urllib.parse import urlparse


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


_classes = {
    'paper': [Paper, paper],
    'project': [Project, project],
    'whitepaper': [WhitePaper, paper],
    'deliverable': [Deliverable, paper],
}


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns an object (that can be used via kwargs)
    if the user passes, None otherwise
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            obj = test_func(request, *args, **kwargs)
            if obj:
                kwargs['obj'] = obj
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def index(request):
    return HttpResponse("Protasis CollabTool")


def check_user(r, *args, **kwargs):
    cl = kwargs['cl']
    if cl not in _classes:
        return HttpResponseNotFound()
    _opts = _classes[cl]

    obj = get_object_or_404(_opts[0], pk=kwargs['id'])
    u = r.user
    user_groups = u.groups.all()
    if u.is_authenticated and obj.group_access.filter(pk__in=map(lambda x: x.id, user_groups)):
        return obj
    else:
        return None


# we need a decorator to check credentials
def check_group_access(function=None):
    actual_decorator = user_passes_test(check_user)
    if function:
        return actual_decorator(function)
    return actual_decorator


def check_data(r, *args, **kwargs):
    h = kwargs['hash']

    obj = get_object_or_404(Data, sha512=h)
    u = r.user
    user_groups = u.groups.all()
    if u.is_authenticated and obj.group_access.filter(pk__in=map(lambda x: x.id, user_groups)):
        return obj
    else:
        return None


# we need a decorator to check credentials
def check_data_access(function=None):
    # from IPython import embed
    # embed()
    actual_decorator = user_passes_test(check_data)
    if function:
        return actual_decorator(function)
    return actual_decorator


@check_group_access()
def get(request, cl, *args, **kwargs):
    _view = _classes[cl][1]

    return _view(request, kwargs['obj'])


def serve_static(request, path, *args, **kwargs):
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


@check_data_access()
def protected_data(request, hash, filename, obj=None):
    # set PRIVATE_MEDIA_ROOT to the root folder of your private media files
    import os

    d = obj
    f = os.path.split(d.data.name)[-1]

    from IPython import embed
    embed()
    if filename != f:
        return HttpResponse(status=404)
    return serve_static(request, f)
