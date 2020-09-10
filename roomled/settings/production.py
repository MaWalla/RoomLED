from django.core.exceptions import ImproperlyConfigured
import os
from .base import *

DEBUG = False

secret_key_env = os.path.expandvars('${DJANGO_SECRET_KEY}')
if secret_key_env == '${DJANGO_SECRET_KEY}':
    raise ImproperlyConfigured('You need to set a secret key in your environmental variables under DJANGO_SECRET_KEY')
else:
    SECRET_KEY = secret_key_env

roomled_host_env = os.path.expandvars('${ROOMLED_HOST}')
if roomled_host_env == '${ROOMLED_HOST}':
    raise ImproperlyConfigured('You need to set your host in your environmental variables under ROOMLED_HOST')
else:
    ALLOWED_HOSTS = [roomled_host_env]
