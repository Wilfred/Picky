import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "picky.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from dj_static import Cling

application = Cling(Sentry(get_wsgi_application()))
