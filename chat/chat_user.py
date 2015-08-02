from django.conf import settings
from django.db import models


class ChatUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    class Meta:
        app_label = 'chat'
        managed = True
