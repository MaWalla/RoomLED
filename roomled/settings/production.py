from django.core.exceptions import ImproperlyConfigured
import os
from .base import *

DEBUG = False

secret_key_env = os.path.expandvars('${DJANGO_SECRET_KEY}')
if secret_key_env == '${DJANGO_SECRET_KEY}':
    raise ImproperlyConfigured('You need to set a secret key in your environmental variables under DJANGO_SECRET_KEY')
else:
    SECRET_KEY = secret_key_env

ALLOWED_HOSTS = ['mawalla.servebeer.com']
