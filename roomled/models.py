from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class RoomLEDUser(AbstractUser):
    pass


class Device(models.Model):
    ip = models.CharField(_('IP address'), max_length=15)
    port = models.IntegerField(_('port'))
    leds = models.IntegerField(_('leds'))
    name = models.CharField(_('name'), max_length=64)

    def __str__(self):
        return self.name
