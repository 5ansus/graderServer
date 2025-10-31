"""
WSGI config for PythonAnywhere
This file should be placed in /var/www/ directory in PythonAnywhere
Update the path to your project directory
"""

import sys
import os

# Añade el directorio de tu proyecto al path
# IMPORTANTE: Cambia 'YOUR_USERNAME' por tu nombre de usuario en PythonAnywhere
project_home = '/home/YOUR_USERNAME/HaloweenServer'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importa la aplicación Flask
from app import app as application

# Set secret key from environment variable (set this in PythonAnywhere web app settings)
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')
