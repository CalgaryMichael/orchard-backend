import os
import django_heroku
from .base import *

django_heroku.settings(locals())

BATCH_SIZE = 10000
ALLOWED_HOSTS = ['powerful-coast-21514.herokuapp.com']

PROJECT_ROOT = os.path.join(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
