# Django Server - Guía Rápida de Inicio

## 🚀 Inicio Rápido (Windows)

### 1. Instalar dependencias
```powershell
cd django_server
pip install -r requirements.txt
```

### 2. Configurar base de datos
```powershell
python manage.py migrate
```

### 3. Crear superusuario
```powershell
python manage.py createsuperuser
```

### 4. Cargar challenges
```powershell
python load_challenges.py
```

### 5. Ejecutar servidor
```powershell
python manage.py runserver
```

Visita:
- API: http://127.0.0.1:8000/api/health
- Admin: http://127.0.0.1:8000/admin/

## ✨ Añadir Nuevos Challenges

### Opción 1: Desde el Admin (Más Fácil)
1. Ve a http://127.0.0.1:8000/admin/
2. Login
3. Click "Challenges" → "Add Challenge"
4. Rellena los campos y guarda

### Opción 2: Por Código
1. Edita `grader/evaluators.py` y añade tu función de evaluación:
```python
@staticmethod
def evaluate_challenge_6(code: str) -> tuple[int, bool, str, float]:
    # Tu lógica aquí
    pass
```

2. Añádelo al diccionario de evaluators
3. Crea el challenge en el admin

## 📚 Documentación Completa

Ver `README_DJANGO.md` para instrucciones detalladas y deployment en PythonAnywhere.
