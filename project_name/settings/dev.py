from . import get_env_variable
from .base import *

DEBUG = bool(get_env_variable('DEBUG', True))
SECRET_KEY = 'notsosecret'

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

####################
# COMPASS SETTINGS #
####################

# The config for SASS is in config.rb
RUNPROCESS_PROCESSES = (
    ('compass', 'watch', '--poll'),
)
