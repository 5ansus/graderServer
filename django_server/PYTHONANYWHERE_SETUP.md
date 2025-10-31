# 🚀 Guía de Deployment en PythonAnywhere - Configuración Manual

## 📋 Pasos para desplegar con "Manual Configuration"

### 1️⃣ Subir el código a PythonAnywhere

#### Opción A: Con Git Clone (RECOMENDADO)

En la consola Bash de PythonAnywhere:

```bash
cd ~
git clone https://github.com/5ansus/graderServer.git
cd graderServer/django_server
```

#### Opción B: Subir archivos manualmente

1. Ve a la pestaña **"Files"** en PythonAnywhere
2. Crea directorio `graderServer`
3. Sube toda la carpeta `django_server`

---

### 2️⃣ Instalar dependencias

En la consola Bash de PythonAnywhere:

```bash
cd ~/graderServer/django_server
pip3.10 install --user -r requirements.txt
```

Esto instalará:
- Django
- Django REST Framework
- django-cors-headers
- PyJWT

---

### 3️⃣ Configurar la base de datos

```bash
cd ~/graderServer/django_server
python3.10 manage.py makemigrations
python3.10 manage.py migrate
```

Esto creará el archivo `db.sqlite3` con las tablas necesarias.

---

### 4️⃣ Crear superusuario (para acceder al admin)

```bash
python3.10 manage.py createsuperuser
```

Te pedirá:
- Username (ejemplo: admin)
- Email (opcional, puedes dejar en blanco)
- Password (mínimo 8 caracteres)

---

### 5️⃣ Cargar los challenges iniciales

```bash
python3.10 load_challenges.py
```

Esto cargará los 5 challenges base en la base de datos.

---

### 6️⃣ Crear Web App en PythonAnywhere

1. Ve a la pestaña **"Web"**
2. Click en **"Add a new web app"**
3. Selecciona **"Manual configuration"** (que ya hiciste ✅)
4. Selecciona **"Python 3.10"**
5. Click "Next" hasta finalizar

---

### 7️⃣ Configurar el archivo WSGI

**IMPORTANTE**: Este es el paso clave para la configuración manual.

1. En la pestaña **"Web"**, busca la sección **"Code"**
2. Verás un enlace al archivo WSGI, algo como:
   ```
   /var/www/TU_USERNAME_pythonanywhere_com_wsgi.py
   ```
3. **Haz click en ese enlace** para editar el archivo

4. **BORRA TODO** el contenido del archivo

5. **Copia y pega** este código (reemplazando `YOUR_USERNAME` con tu usuario):

```python
# +++++++++++ DJANGO +++++++++++
# Django WSGI configuration for PythonAnywhere

import os
import sys

# Añade el path de tu proyecto Django
# IMPORTANTE: Reemplaza 'YOUR_USERNAME' con tu nombre de usuario de PythonAnywhere
path = '/home/YOUR_USERNAME/graderServer/django_server'
if path not in sys.path:
    sys.path.insert(0, path)

# Configura el settings de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'halloween_server.settings'

# Importa la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Ejemplo real**: Si tu usuario es `UAMCPrA`, quedaría:
```python
path = '/home/UAMCPrA/graderServer/django_server'
```

6. Click **"Save"** (arriba a la derecha)

---

### 8️⃣ Configurar archivos estáticos

En la pestaña **"Web"**, busca la sección **"Static files"**.

Click en **"Enter URL"** y **"Enter path"** para añadir:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/graderServer/django_server/staticfiles` |
| `/admin/static/` | `/home/YOUR_USERNAME/.local/lib/python3.10/site-packages/django/contrib/admin/static` |

Luego en la consola Bash:
```bash
cd ~/graderServer/django_server
python3.10 manage.py collectstatic --noinput
```

---

### 9️⃣ Configurar variables de entorno (OPCIONAL pero recomendado)

En la pestaña **"Web"**, busca **"Environment variables"** y añade:

| Variable | Valor |
|----------|-------|
| `SECRET_KEY` | `tu-clave-secreta-aleatoria-2025` |
| `DEBUG` | `False` |
| `ALLOWED_HOST` | `YOUR_USERNAME.pythonanywhere.com` |

**Nota**: Genera una SECRET_KEY aleatoria, por ejemplo: `django-insecure-h8#2k$9mxp@4qw!z7n`

---

### 🔟 Recargar la aplicación

1. Ve a la pestaña **"Web"**
2. Busca el botón verde grande que dice **"Reload YOUR_USERNAME.pythonanywhere.com"**
3. **Haz click en "Reload"**
4. Espera unos segundos

---

### ✅ Verificar que funciona

Abre tu navegador y visita:

```
https://YOUR_USERNAME.pythonanywhere.com/api/health
```

Deberías ver:
```json
{
  "status": "ok",
  "message": "API is running"
}
```

También puedes acceder al admin:
```
https://YOUR_USERNAME.pythonanywhere.com/admin/
```

---

## 🎯 Actualizar el cliente

Edita el archivo `grader_qiskit_client.py`, línea 20:

```python
BASE_URL = "https://YOUR_USERNAME.pythonanywhere.com/api"
```

Por ejemplo, si tu usuario es `UAMCPrA`:
```python
BASE_URL = "https://UAMCPrA.pythonanywhere.com/api"
```

---

## 🧪 Probar la API completa

Desde Python:

```python
from grader_qiskit_client import *

# Test de conexión
test_connection()

# Registrar usuario
register('testuser', 'test@email.com', 'password123')

# Ver challenges
show_challenges()

# Ver leaderboard
show_leaderboard()
```

---

## 🔧 Comandos útiles para mantenimiento

### Ver logs de errores
En PythonAnywhere, pestaña "Web" → **"Error log"** (click para ver)

### Actualizar código después de cambios
```bash
cd ~/graderServer
git pull
cd django_server
python3.10 manage.py migrate  # Si hay cambios en modelos
```

Luego en la pestaña "Web": **Click "Reload"**

### Añadir nuevo challenge
1. Ir a `https://YOUR_USERNAME.pythonanywhere.com/admin/`
2. Login con superusuario
3. Click "Challenges" → "Add Challenge"
4. Rellenar y guardar
5. No necesitas hacer reload

### Ver la base de datos
```bash
cd ~/graderServer/django_server
python3.10 manage.py dbshell
```

O mejor aún, usa el admin de Django.

---

## ⚠️ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'rest_framework'"
```bash
pip3.10 install --user djangorestframework django-cors-headers
```

### Error: "OperationalError: no such table"
```bash
cd ~/graderServer/django_server
python3.10 manage.py migrate
```

### Error 500 en la web
1. Ve a la pestaña "Web"
2. Click en "Error log"
3. Lee el último error
4. Usualmente es un path incorrecto en el WSGI

### La API no guarda datos
Verifica que ejecutaste:
```bash
python3.10 manage.py migrate
```

### No puedo acceder al admin
Verifica que creaste el superusuario:
```bash
python3.10 manage.py createsuperuser
```

---

## 📊 Estructura final en PythonAnywhere

```
/home/YOUR_USERNAME/
└── graderServer/
    └── django_server/
        ├── manage.py
        ├── db.sqlite3                    ← Base de datos
        ├── halloween_server/
        │   ├── settings.py
        │   └── wsgi.py
        ├── grader/
        │   ├── models.py
        │   ├── views.py
        │   └── ...
        └── staticfiles/                  ← Archivos estáticos
```

---

## 🎃 ¡Listo!

Tu API está funcionando en:
- **API Base**: `https://YOUR_USERNAME.pythonanywhere.com/api/`
- **Health Check**: `https://YOUR_USERNAME.pythonanywhere.com/api/health`
- **Admin Panel**: `https://YOUR_USERNAME.pythonanywhere.com/admin/`
- **Challenges**: `https://YOUR_USERNAME.pythonanywhere.com/api/challenges`
- **Leaderboard**: `https://YOUR_USERNAME.pythonanywhere.com/api/leaderboard`

## 🔄 Para actualizar después de cambios

1. **Hacer cambios localmente**
2. **Commit y push a GitHub**:
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push
   ```
3. **En PythonAnywhere**:
   ```bash
   cd ~/graderServer
   git pull
   ```
4. **Reload** en la pestaña Web

---

Happy coding! 🚀
