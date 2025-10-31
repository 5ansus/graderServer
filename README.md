# Halloween Server - Qiskit Grader API

Servidor Flask compatible con `grader_qiskit_client.py` para alojar en PythonAnywhere.

## 📋 Pasos para desplegar en PythonAnywhere

### 1. Crear cuenta en PythonAnywhere
- Ve a https://www.pythonanywhere.com
- Crea una cuenta gratuita o inicia sesión

### 2. Subir archivos

#### Opción A: Usando Git (Recomendado)
En la consola Bash de PythonAnywhere:
```bash
cd ~
git clone <URL_DE_TU_REPOSITORIO> HaloweenServer
cd HaloweenServer
```

#### Opción B: Subir manualmente
- Ve a la pestaña "Files"
- Crea un directorio llamado `HaloweenServer`
- Sube los archivos: `app.py`, `requirements.txt`, `wsgi.py`

### 3. Instalar dependencias

En la consola Bash de PythonAnywhere:
```bash
cd ~/HaloweenServer
pip3.10 install --user -r requirements.txt
```

### 4. Configurar Web App

1. Ve a la pestaña "Web"
2. Haz clic en "Add a new web app"
3. Selecciona **"Flask"** como framework
4. Selecciona **Python 3.10** (o la versión más reciente)
5. Para la ruta del proyecto, usa: `/home/TU_USERNAME/HaloweenServer`

### 5. Configurar WSGI

1. En la pestaña "Web", busca la sección "Code"
2. Haz clic en el archivo WSGI (algo como `/var/www/TU_USERNAME_pythonanywhere_com_wsgi.py`)
3. **Reemplaza TODO el contenido** con el contenido de tu archivo `wsgi.py`
4. **IMPORTANTE**: Cambia `YOUR_USERNAME` por tu nombre de usuario de PythonAnywhere

Ejemplo del contenido del archivo WSGI:
```python
import sys
import os

# Cambia 'UAMCPrA' por TU nombre de usuario
project_home = '/home/UAMCPrA/HaloweenServer'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application

application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key')
```

### 6. Configurar variables de entorno (Opcional pero recomendado)

1. En la pestaña "Web", busca "Environment variables"
2. Añade una variable:
   - Name: `SECRET_KEY`
   - Value: Una clave secreta aleatoria (ej: `tu-clave-super-secreta-2025`)

### 7. Recargar la aplicación

1. En la pestaña "Web"
2. Haz clic en el botón verde **"Reload"**
3. Tu API estará disponible en: `https://TU_USERNAME.pythonanywhere.com`

### 8. Actualizar el cliente

En tu archivo `grader_qiskit_client.py`, la línea 20 ya tiene la URL correcta:
```python
BASE_URL = "https://UAMCPrA.pythonanywhere.com/api"
```

Cambia `UAMCPrA` por tu nombre de usuario de PythonAnywhere.

## 🧪 Probar la API

Puedes probar que funciona visitando:
- `https://TU_USERNAME.pythonanywhere.com/api/health`

Deberías ver una respuesta JSON:
```json
{
  "status": "ok",
  "message": "API is running"
}
```

## 📝 Uso del cliente

```python
from grader_qiskit_client import *

# Registrar usuario
register('username', 'email@example.com', 'password')

# Login
login('username', 'password')

# Ver challenges
show_challenges()

# Enviar solución
submit(1, "tu código aquí")

# Ver progreso
show_progress()

# Ver leaderboard
show_leaderboard()
```

## 🔧 Endpoints disponibles

### Autenticación
- `POST /api/register` - Registrar nuevo usuario
- `POST /api/login` - Iniciar sesión
- `GET /api/profile` - Ver perfil del usuario

### Challenges
- `GET /api/challenges` - Listar todos los challenges
- `GET /api/challenges/<id>` - Ver detalles de un challenge

### Submissions
- `POST /api/submit` - Enviar solución
- `GET /api/submissions` - Ver tus submissions
- `GET /api/submissions/<id>` - Ver detalles de una submission

### Leaderboard
- `GET /api/leaderboard` - Ver tabla de clasificación
- `GET /api/progress` - Ver tu progreso
- `GET /api/stats` - Ver estadísticas generales

### Health Check
- `GET /api/health` - Verificar que la API está funcionando

## ⚠️ Importante

1. **Límites de cuenta gratuita**: PythonAnywhere gratuito tiene limitaciones
2. **Base de datos**: Actualmente usa diccionarios en memoria. Para producción, implementa una base de datos real (SQLite, MySQL, etc.)
3. **Seguridad**: Cambia el `SECRET_KEY` en producción
4. **Evaluación de código**: Implementa tu propia lógica en la función `evaluate_code()`

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
cd ~/HaloweenServer
pip3.10 install --user -r requirements.txt
```

### Error: "ImportError: cannot import name 'app'"
Verifica que el archivo WSGI tenga la ruta correcta a tu proyecto.

### Error 401: "Token is missing"
Ejecuta `login('username', 'password')` antes de usar otras funciones.

### La API no responde
1. Revisa los logs de error en la pestaña "Web" de PythonAnywhere
2. Haz clic en "Reload" en la pestaña "Web"
3. Verifica que todas las dependencias estén instaladas

## 📞 Soporte

Si tienes problemas, contacta a los co-organizadores de MadQFF'25 (usuarios con nombre púrpura o rojo en Discord).
