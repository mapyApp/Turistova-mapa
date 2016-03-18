"""
WSGI config for turistickaMapa project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
sys.path = ['/home/turisti/Turistova-mapa/src'] + sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turistickaMapa.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
