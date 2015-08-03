from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
import requests

from chat.model.chat_user import ChatUser


class BackendBase(object):
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class BasicChatBackend(BackendBase):
    @transaction.atomic
    def authenticate(self, username=None, password=None, **kwargs):
        if not username or not password:
            return

        r = requests.get(settings.CHAT_BASE + 'rest/profile', auth=(username, password))
        if r.status_code == 200:
            return ChatUser.from_profile(r.json(), username)
        else:
            return None


class TransparentChatAuthenticationBackend(BackendBase):
    @transaction.atomic
    def authenticate(self, sid=None, **kwargs):
        if not sid:
            return

        r = requests.get(settings.CHAT_BASE + 'rest/profile', cookies={"sid": sid}, verify=False)
        if r.status_code == 200:
            profile = r.json()
            return ChatUser.from_profile(r.json(), profile["user"]["name"])
        else:
            return None
