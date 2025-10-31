# Halloween Server - Django API con Base de Datos

Servidor Django REST API completo con base de datos SQLite para el sistema de grader de Qiskit.

## ✨ Ventajas sobre Flask

- ✅ **Base de datos integrada** (SQLite por defecto, fácil migrar a PostgreSQL/MySQL)
- ✅ **Panel de administración** automático para gestionar challenges y submissions
- ✅ **ORM potente** para consultas complejas
- ✅ **Fácil añadir nuevos challenges** desde el admin o código
- ✅ **Sistema de autenticación robusto**
- ✅ **Migraciones automáticas** de base de datos

## 📋 Estructura del Proyecto

```
django_server/
├── manage.py                          # Script de gestión de Django
├── requirements.txt                   # Dependencias
├── halloween_server/                  # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py                    # Configuración principal
│   ├── urls.py                        # URLs principales
│   └── wsgi.py                        # Configuración WSGI para PythonAnywhere
└── grader/                            # App principal
    ├── __init__.py
    ├── models.py                      # Modelos: Challenge, Submission, UserProfile
    ├── serializers.py                 # Serializers para la API
    ├── views.py                       # Vistas de la API
    ├── urls.py                        # URLs de la API
    ├── admin.py                       # Configuración del admin
    ├── evaluators.py                  # Lógica de evaluación de código
    └── apps.py                        # Configuración de la app
```

## 🚀 Instalación Local (Desarrollo)

### 1. Instalar dependencias

```powershell
cd django_server
pip install -r requirements.txt
```

### 2. Crear base de datos y hacer migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear superusuario (para acceder al admin)

```powershell
python manage.py createsuperuser
```

### 4. Cargar challenges iniciales (opcional)

Crea un archivo `load_challenges.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'halloween_server.settings')
django.setup()

from grader.models import Challenge

challenges_data = [
    {
        'id': 1,
        'name': 'Challenge 1: Basic Operations',
        'description': 'Implementa una función básica',
        'max_score': 100,
        'difficulty': 'easy'
    },
    {
        'id': 2,
        'name': 'Challenge 2: Intermediate',
        'description': 'Implementa algo más complejo',
        'max_score': 100,
        'difficulty': 'medium'
    },
    # ... más challenges
]

for ch_data in challenges_data:
    Challenge.objects.update_or_create(
        id=ch_data['id'],
        defaults=ch_data
    )

print("Challenges cargados!")
```

```powershell
python load_challenges.py
```

### 5. Correr servidor local

```powershell
python manage.py runserver
```

Visita:
- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

## 📦 Deployment en PythonAnywhere

### 1. Subir archivos

#### Opción A: Con Git (Recomendado)
```bash
cd ~
git clone <URL_REPO> HaloweenServer
cd HaloweenServer/django_server
```

#### Opción B: Manualmente
Sube la carpeta `django_server` completa a PythonAnywhere.

### 2. Instalar dependencias

En la consola Bash de PythonAnywhere:
```bash
cd ~/HaloweenServer/django_server
pip3.10 install --user -r requirements.txt
```

### 3. Configurar base de datos

```bash
cd ~/HaloweenServer/django_server
python3.10 manage.py makemigrations
python3.10 manage.py migrate
python3.10 manage.py createsuperuser
```

### 4. Crear Web App

1. Ve a la pestaña **"Web"**
2. Click en **"Add a new web app"**
3. Selecciona **"Manual configuration"** (NO Django)
4. Selecciona **Python 3.10**

### 5. Configurar WSGI

En la pestaña "Web", encuentra la sección "Code" y edita el archivo WSGI:

```python
import os
import sys

# Añade el path de tu proyecto
path = '/home/YOUR_USERNAME/HaloweenServer/django_server'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'halloween_server.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**IMPORTANTE**: Cambia `YOUR_USERNAME` por tu usuario de PythonAnywhere.

### 6. Configurar archivos estáticos

En la pestaña "Web", sección "Static files":

| URL          | Directory                                                    |
|--------------|--------------------------------------------------------------|
| /static/     | /home/YOUR_USERNAME/HaloweenServer/django_server/staticfiles |

Luego en la consola:
```bash
cd ~/HaloweenServer/django_server
python3.10 manage.py collectstatic --noinput
```

### 7. Variables de entorno (Recomendado)

En la pestaña "Web" → "Environment variables":
- `SECRET_KEY`: Una clave secreta aleatoria
- `DEBUG`: False
- `ALLOWED_HOST`: YOUR_USERNAME.pythonanywhere.com

### 8. Recargar

Click en el botón verde **"Reload"** en la pestaña Web.

Tu API estará en: `https://YOUR_USERNAME.pythonanywhere.com/api/`

## 🎯 Cómo Añadir Nuevos Challenges

### Opción 1: Desde el Admin de Django (MÁS FÁCIL)

1. Ve a `https://YOUR_USERNAME.pythonanywhere.com/admin/`
2. Login con tu superusuario
3. Click en "Challenges" → "Add Challenge"
4. Rellena:
   - **ID**: 6 (o el siguiente número)
   - **Name**: "Challenge 6: Tu título"
   - **Description**: Descripción del ejercicio
   - **Max Score**: 100
   - **Difficulty**: easy/medium/hard
   - **Is Active**: ✓
5. Click "Save"

### Opción 2: Por Código

En `grader/evaluators.py`, añade un nuevo método:

```python
@staticmethod
def evaluate_challenge_6(code: str) -> tuple[int, bool, str, float]:
    """
    Evalúa el Challenge 6 - Tu nuevo ejercicio
    """
    start_time = time.time()

    try:
        local_scope = {}
        exec(code, {}, local_scope)

        # Tu lógica de evaluación aquí
        # ...

        score = 100
        passed = True
        feedback = "¡Perfecto!"

        execution_time = time.time() - start_time
        return score, passed, feedback, execution_time

    except Exception as e:
        execution_time = time.time() - start_time
        return 0, False, f"Error: {str(e)}", execution_time
```

Y añádelo al diccionario de evaluators:

```python
evaluators = {
    1: CodeEvaluator.evaluate_challenge_1,
    2: CodeEvaluator.evaluate_challenge_2,
    3: CodeEvaluator.evaluate_challenge_3,
    4: CodeEvaluator.evaluate_challenge_4,
    5: CodeEvaluator.evaluate_challenge_5,
    6: CodeEvaluator.evaluate_challenge_6,  # ← NUEVO
}
```

Luego crea el challenge en el admin o por código.

## 📊 Panel de Administración

Accede a `/admin/` para:
- ✅ Ver todas las submissions
- ✅ Ver usuarios y sus scores
- ✅ Crear/editar/eliminar challenges
- ✅ Ver estadísticas
- ✅ Filtrar y buscar submissions
- ✅ Exportar datos

## 🔌 Endpoints de la API

Todos los endpoints están en `/api/`:

### Autenticación
- `POST /api/register` - Registrar usuario
- `POST /api/login` - Login
- `GET /api/profile` - Ver perfil (requiere token)

### Challenges
- `GET /api/challenges` - Listar challenges
- `GET /api/challenges/<id>` - Ver detalles de un challenge

### Submissions
- `POST /api/submit` - Enviar código
  ```json
  {
    "challenge_id": 1,
    "code": "def solution(x):\n    return x * 2"
  }
  ```
- `GET /api/submissions` - Ver tus submissions
- `GET /api/submissions?challenge_id=1` - Filtrar por challenge
- `GET /api/submissions/<id>` - Ver detalles de una submission

### Leaderboard
- `GET /api/leaderboard?limit=50` - Ver ranking
- `GET /api/progress` - Ver tu progreso
- `GET /api/stats` - Estadísticas generales

### Health Check
- `GET /api/health` - Verificar que la API funciona

## 💾 Base de Datos

El proyecto usa **SQLite** por defecto (archivo `db.sqlite3`).

### Modelos principales:

1. **Challenge**: Los ejercicios
   - id, name, description, max_score, difficulty, is_active

2. **Submission**: Código enviado por usuarios
   - user, challenge, code, score, passed, feedback, submitted_at

3. **UserProfile**: Información adicional del usuario
   - user, total_score, created_at

### Ver datos en la DB:

```bash
python manage.py dbshell
```

O usa el admin de Django.

## 🔧 Comandos Útiles

```bash
# Crear migraciones después de cambiar modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Colectar archivos estáticos
python manage.py collectstatic

# Abrir shell de Django
python manage.py shell

# Ver SQL de las migraciones
python manage.py sqlmigrate grader 0001
```

## 🧪 Probar la API

### Con curl:

```bash
# Health check
curl https://YOUR_USERNAME.pythonanywhere.com/api/health

# Register
curl -X POST https://YOUR_USERNAME.pythonanywhere.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'

# Login
curl -X POST https://YOUR_USERNAME.pythonanywhere.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

### Con el cliente Python:

El cliente `grader_qiskit_client.py` ya es compatible. Solo actualiza la URL en la línea 20:

```python
BASE_URL = "https://YOUR_USERNAME.pythonanywhere.com/api"
```

## 📝 Actualizar URL en el Cliente

Edita `grader_qiskit_client.py`, línea 20:

```python
BASE_URL = "https://YOUR_USERNAME.pythonanywhere.com/api"
```

## ⚠️ Troubleshooting

### Error: "No module named 'rest_framework'"
```bash
pip3.10 install --user djangorestframework
```

### Error: "OperationalError: no such table"
```bash
python3.10 manage.py migrate
```

### Error 500 en producción
1. Mira los logs en PythonAnywhere (pestaña Web → Error log)
2. Verifica que `DEBUG = False` en producción
3. Verifica que `ALLOWED_HOSTS` incluye tu dominio

### La API no guarda datos
Verifica que ejecutaste las migraciones:
```bash
python3.10 manage.py migrate
```

## 🔐 Seguridad

En producción:
1. ✅ Cambia `SECRET_KEY` a algo aleatorio
2. ✅ Pon `DEBUG = False`
3. ✅ Configura `ALLOWED_HOSTS` correctamente
4. ✅ Usa HTTPS (PythonAnywhere lo hace automáticamente)

## 📞 Soporte

Si tienes problemas, contacta a los co-organizadores de MadQFF'25.

## 🎃 Happy Coding!
