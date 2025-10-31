# ✅ Checklist de Deployment - PythonAnywhere

## Antes de empezar
- [ ] Tienes cuenta en PythonAnywhere
- [ ] Has seleccionado "Manual Configuration" con Python 3.10
- [ ] Tu código está en GitHub (opcional pero recomendado)

## Paso 1: Subir el código
- [ ] Abrir consola Bash en PythonAnywhere
- [ ] Ejecutar: `git clone URL_DE_TU_REPO HaloweenServer`
- [ ] Ejecutar: `cd HaloweenServer/django_server`

## Paso 2: Setup automático
- [ ] Ejecutar: `bash setup_pythonanywhere.sh`
- [ ] O manualmente:
  - [ ] `pip3.10 install --user -r requirements.txt`
  - [ ] `python3.10 manage.py migrate`
  - [ ] `python3.10 load_challenges.py`
  - [ ] `python3.10 manage.py collectstatic --noinput`

## Paso 3: Crear superusuario
- [ ] Ejecutar: `python3.10 manage.py createsuperuser`
- [ ] Anotar usuario y contraseña

## Paso 4: Configurar WSGI
- [ ] Ir a pestaña "Web" en PythonAnywhere
- [ ] Click en el archivo WSGI (en sección "Code")
- [ ] Borrar TODO el contenido
- [ ] Copiar código de `WSGI_CODE.txt`
- [ ] Reemplazar `YOUR_USERNAME` con tu usuario
- [ ] Click "Save"

## Paso 5: Configurar archivos estáticos
- [ ] En pestaña "Web", sección "Static files"
- [ ] Añadir entrada:
  - URL: `/static/`
  - Directory: `/home/YOUR_USERNAME/HaloweenServer/django_server/staticfiles`

## Paso 6: Reload
- [ ] Click en botón verde "Reload YOUR_USERNAME.pythonanywhere.com"
- [ ] Esperar unos segundos

## Paso 7: Verificar
- [ ] Abrir: `https://YOUR_USERNAME.pythonanywhere.com/api/health`
- [ ] Debe mostrar: `{"status": "ok", "message": "API is running"}`
- [ ] Abrir: `https://YOUR_USERNAME.pythonanywhere.com/admin/`
- [ ] Login con superusuario

## Paso 8: Actualizar cliente
- [ ] Editar `grader_qiskit_client.py` línea 20
- [ ] Cambiar a: `BASE_URL = "https://YOUR_USERNAME.pythonanywhere.com/api"`

## Paso 9: Probar
- [ ] Ejecutar: `python -c "from grader_qiskit_client import test_connection; test_connection()"`
- [ ] Registrar usuario de prueba
- [ ] Ver challenges
- [ ] Enviar una submission de prueba

## ✅ ¡LISTO!

### URLs importantes:
- API: `https://YOUR_USERNAME.pythonanywhere.com/api/`
- Admin: `https://YOUR_USERNAME.pythonanywhere.com/admin/`
- Health: `https://YOUR_USERNAME.pythonanywhere.com/api/health`
- Challenges: `https://YOUR_USERNAME.pythonanywhere.com/api/challenges`

### Para añadir nuevos challenges:
1. Ir al admin
2. Click "Challenges" → "Add Challenge"
3. Rellenar formulario
4. No necesitas hacer reload

### Para ver logs de errores:
- Pestaña "Web" → "Error log"

### Para actualizar código:
```bash
cd ~/HaloweenServer
git pull
# Click "Reload" en pestaña Web
```

🎃 Happy Halloween Coding!
