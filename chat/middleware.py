from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured


class ChatSessionAuthenticationMiddleware(object):
    _cachedNames = {}

    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured()

        sid = request.COOKIES.get('sid', None)

        if not sid:
            if request.user.is_authenticated() and request.session.get('chat', False):
                auth.logout(request)
            return

        if request.user.is_authenticated():
            return

        user = auth.authenticate(sid=sid)
        if user:
            request.user = user
            auth.login(request, user)
            request.session['chat'] = True
