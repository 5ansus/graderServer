#!/bin/bash
# Script de setup para PythonAnywhere
# Ejecuta este script después de hacer git clone

echo "🎃 Halloween Server - Setup Script"
echo "===================================="
echo ""

# Detectar usuario automáticamente
USERNAME=$(whoami)
echo "✓ Usuario detectado: $USERNAME"
echo ""

# Ir al directorio del proyecto
cd ~/HaloweenServer/django_server
echo "✓ Directorio: $(pwd)"
echo ""

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip3.10 install --user -r requirements.txt
echo ""

# Crear base de datos
echo "🗄️  Creando base de datos..."
python3.10 manage.py makemigrations
python3.10 manage.py migrate
echo ""

# Cargar challenges
echo "📝 Cargando challenges iniciales..."
python3.10 load_challenges.py
echo ""

# Colectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python3.10 manage.py collectstatic --noinput
echo ""

echo "✅ Setup completado!"
echo ""
echo "⚠️  SIGUIENTE PASO:"
echo "1. Crea un superusuario con:"
echo "   python3.10 manage.py createsuperuser"
echo ""
echo "2. Configura el archivo WSGI en la pestaña Web con:"
echo "   path = '/home/$USERNAME/HaloweenServer/django_server'"
echo ""
echo "3. Configura archivos estáticos en la pestaña Web:"
echo "   URL: /static/"
echo "   Directory: /home/$USERNAME/HaloweenServer/django_server/staticfiles"
echo ""
echo "4. Haz click en 'Reload' en la pestaña Web"
echo ""
echo "Tu API estará en: https://$USERNAME.pythonanywhere.com/api/"
echo ""
echo "🎃 Happy Halloween Coding!"
