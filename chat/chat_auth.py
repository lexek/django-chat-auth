from django.conf import settings

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction
import requests

from chat.chat_user import ChatUser


class ChatBackend(object):
    @transaction.atomic
    def authenticate(self, username=None, password=None):
        r = requests.get(settings.CHAT_BASE + 'rest/profile', auth=(username, password))

        if r.status_code == 200:
            data = r.json()
            try:
                chat_user = ChatUser.objects.get(id=data["user"]["id"])
                self.__fill_user(chat_user.user, data, password)
            except ChatUser.DoesNotExist:
                user = User.objects.create_user(username)
                self.__fill_user(user, data, password)
                chat_user = ChatUser()
                chat_user.id = data["user"]["id"]
                chat_user.user = user
                chat_user.save()
            return chat_user.user
        else:
            return None

    @staticmethod
    def __fill_user(user, data, password):
        role = data["user"]["role"]
        user.password = make_password(password)
        user.username = data["user"]["name"]
        admin = role == "SUPERADMIN"
        user.is_superuser = user.is_superuser or admin
        user.is_staff = user.is_staff or admin
        user.is_active = True
        user.save()

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
