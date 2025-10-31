# 🚀 COMANDOS RÁPIDOS - Copy & Paste

## 📝 Repo: github.com/5ansus/graderServer

---

## EN PYTHONANYWHERE - Consola Bash

### Paso 1: Clonar y setup
```bash
cd ~
git clone https://github.com/5ansus/graderServer.git
cd graderServer/django_server
```

### Paso 1b: Setup manual (si el script falla)
```bash
# Instalar dependencias
pip3.10 install --user -r requirements.txt

# Crear migraciones
python3.10 manage.py makemigrations grader
python3.10 manage.py migrate

# Cargar challenges
python3.10 load_challenges.py

# Colectar estáticos
python3.10 manage.py collectstatic --noinput
```

### O usar el script automático:
```bash
bash setup_pythonanywhere.sh
```

### Paso 2: Crear superusuario
```bash
python3.10 manage.py createsuperuser
```
(Introduce username, email, password)

---

## EN PYTHONANYWHERE - Web UI

### Paso 3: Configurar WSGI

**Pestaña "Web" → Sección "Code" → Click en archivo WSGI**

**BORRA TODO** y pega esto (cambia YOUR_USERNAME por tu usuario):

```python
import os
import sys

path = '/home/YOUR_USERNAME/graderServer/django_server'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'halloween_server.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Ejemplo si tu usuario es `UAMCPrA`:
```python
path = '/home/UAMCPrA/graderServer/django_server'
```

**Click "Save"**

---

### Paso 4: Configurar Static Files

**Pestaña "Web" → Sección "Static files" → Click "Enter URL" y "Enter path"**

**URL:**
```
/static/
```

**Directory (cambia YOUR_USERNAME):**
```
/home/YOUR_USERNAME/graderServer/django_server/staticfiles
```

Ejemplo si tu usuario es `UAMCPrA`:
```
/home/UAMCPrA/graderServer/django_server/staticfiles
```

---

### Paso 5: Reload

**Pestaña "Web" → Click botón verde "Reload YOUR_USERNAME.pythonanywhere.com"**

---

## ✅ VERIFICAR

Abre en navegador:
```
https://YOUR_USERNAME.pythonanywhere.com/api/health
```

Debe mostrar:
```json
{"status": "ok", "message": "API is running"}
```

Admin:
```
https://YOUR_USERNAME.pythonanywhere.com/admin/
```

---

## 📝 ACTUALIZAR grader_qiskit_client.py

Línea 20, cambia a:
```python
BASE_URL = "https://YOUR_USERNAME.pythonanywhere.com/api"
```

---

## 🔄 PARA ACTUALIZAR DESPUÉS

```bash
cd ~/graderServer
git pull
```

Luego: **Pestaña "Web" → Click "Reload"**

---

## 🎃 ¡LISTO!

URLs importantes:
- API: https://YOUR_USERNAME.pythonanywhere.com/api/
- Health: https://YOUR_USERNAME.pythonanywhere.com/api/health
- Admin: https://YOUR_USERNAME.pythonanywhere.com/admin/
- Challenges: https://YOUR_USERNAME.pythonanywhere.com/api/challenges
- Leaderboard: https://YOUR_USERNAME.pythonanywhere.com/api/leaderboard
