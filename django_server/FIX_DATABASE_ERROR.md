# 🔧 SOLUCIÓN AL ERROR "no such table: grader_challenge"

## El problema
Las migraciones no se ejecutaron correctamente. Las tablas no existen en la base de datos.

## Solución rápida en PythonAnywhere

### Paso 1: Ir al directorio del proyecto
```bash
cd ~/graderServer/django_server
```

### Paso 2: Borrar la base de datos anterior (si existe)
```bash
rm -f db.sqlite3
```

### Paso 3: Crear las migraciones para la app grader
```bash
python3.10 manage.py makemigrations grader
```

Deberías ver algo como:
```
Migrations for 'grader':
  grader/migrations/0001_initial.py
    - Create model Challenge
    - Create model UserProfile
    - Create model Submission
```

### Paso 4: Aplicar todas las migraciones
```bash
python3.10 manage.py migrate
```

Deberías ver:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, grader, sessions, authtoken
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying grader.0001_initial... OK
```

### Paso 5: Verificar que las tablas existen
```bash
python3.10 manage.py dbshell
```

Luego ejecuta:
```sql
.tables
```

Deberías ver tablas como:
- grader_challenge
- grader_submission
- grader_userprofile
- auth_user
- etc.

Escribe `.quit` para salir.

### Paso 6: Cargar los challenges
```bash
python3.10 load_challenges.py
```

Ahora debería funcionar y mostrar:
```
Cargando challenges...
✅ Challenge 1 creado: Challenge 1: Introducción
✅ Challenge 2 creado: Challenge 2: Intermedio
...
```

### Paso 7: Crear superusuario
```bash
python3.10 manage.py createsuperuser
```

### Paso 8: Colectar archivos estáticos
```bash
python3.10 manage.py collectstatic --noinput
```

### Paso 9: Configurar WSGI y Reload
- Configura el WSGI (como dice en COMANDOS_RAPIDOS.md)
- Configura static files
- Click "Reload"

---

## ✅ Verificar

Abre en navegador:
```
https://uamcpra.pythonanywhere.com/api/health
```

Admin:
```
https://uamcpra.pythonanywhere.com/admin/
```

---

## 📝 NOTA: Actualización del código

El archivo `settings.py` fue actualizado para usar `'grader.apps.GraderConfig'` en lugar de solo `'grader'`.

Si ya hiciste `git push`, haz `git pull` en PythonAnywhere para obtener los cambios:

```bash
cd ~/graderServer
git pull
cd django_server
```

Y repite los pasos desde el principio.

---

## 🎃 Después de esto, todo debería funcionar correctamente!
