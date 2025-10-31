"""
WSGI config for halloween_server project for PythonAnywhere.
"""

import os
import sys

# Añade el directorio del proyecto al path
# IMPORTANTE: Cambia 'YOUR_USERNAME' por tu nombre de usuario en PythonAnywhere
project_home = '/home/YOUR_USERNAME/HaloweenServer/django_server'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'halloween_server.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
