from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models


class ChatUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    @staticmethod
    def from_profile(profile, username):
        try:
            chat_user = ChatUser.objects.get(id=profile['user']['id'])
            ChatUser.__fill_user(chat_user.user, profile)
        except ChatUser.DoesNotExist:
            user = User.objects.create_user(username)
            ChatUser.__fill_user(user, profile)
            chat_user = ChatUser()
            chat_user.id = profile['user']['id']
            chat_user.user = user
            chat_user.save()
        return chat_user.user

    @staticmethod
    def __fill_user(user, profile):
        role = profile['user']['role']
        user.password = make_password(None)
        user.username = profile['user']['name'] + '@chat'
        admin = role == 'SUPERADMIN'
        user.is_superuser = user.is_superuser or admin
        user.is_staff = user.is_staff or admin
        user.is_active = True
        user.save()

    class Meta:
        app_label = 'chat'
        managed = True

