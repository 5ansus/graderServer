# 🎃 USO SIMPLE DEL HALLOWEEN CHALLENGE

## 🚀 Super Simple - Sin Registro Previo

Los usuarios NO necesitan registrarse previamente. Solo necesitan elegir un username y usarlo.

### ✨ Modo más simple (recomendado)

```python
from grader_qiskit_client import login, submit, show_challenges, show_leaderboard

# Solo con tu username (se crea automáticamente si no existe)
login('tu_nombre')

# Ver challenges disponibles
show_challenges()

# Enviar tu solución
submit(35, "tu código aquí")

# Ver el ranking
show_leaderboard()
```

### 📝 Explicación del sistema

1. **Primera vez**: Cuando haces `login('tu_nombre')`, el sistema:
   - Busca si existe el usuario 'tu_nombre'
   - Si NO existe, lo crea automáticamente
   - Te da un token para enviar submissions

2. **Siguientes veces**:
   - Solo haces `login('tu_nombre')` con el mismo nombre
   - El sistema te reconoce y te da acceso

### 🎯 Flujo completo de ejemplo

```python
from grader_qiskit_client import *

# 1. Login (auto-registro si no existes)
login('AliceQuantum')
# ✅ Welcome AliceQuantum! User created successfully 'AliceQuantum'

# 2. Ver qué challenge hay
show_challenges()
#
# ============= CHALLENGES =================
#
# ✅ Challenge 35: A Halloween Carol: Quantum Chemistry Mystery
#    Score: No intentado

# 3. Hacer tu código en el notebook Halloween35.ipynb
# ... trabajas en el notebook ...

# 4. Enviar tu solución
code = '''
alpha_vqe_result = ...
beta_vqe_result = ...
alpha_gap_ev = 4.5
beta_gap_ev = 2.3
alpha_homo_lumo = 0.165
beta_homo_lumo = 0.085
'''

submit(35, code)
# ✅ Score: 70/100
# Feedback: ...

# 5. Ver el leaderboard
show_leaderboard()
#
# ============= LEADERBOARD ==========
#
# You are at: #5
#
# 🥇  1. AliceQuantum        | 100 pts | 1 challenges
# 🥈  2. BobCircuit          |  95 pts | 1 challenges
# ...

# 6. Ver tu progreso
show_progress()
```

## 🔑 Con password personalizada (opcional)

Si quieres usar una password específica:

```python
# Primera vez - se crea con tu password
login('tu_nombre', 'mi_password_secreta')

# Siguientes veces - usa la misma password
login('tu_nombre', 'mi_password_secreta')
```

## ⚠️ Importante

- **El username es único**: Si alguien más usa 'AliceQuantum' primero, tú no podrás usarlo
- **Elige un nombre único**: Usa algo como 'AliceQuantum_UAM' o 'Alice2025'
- **Sin registro necesario**: El primer `login()` crea tu cuenta automáticamente
- **Token guardado**: Después del primer login, el token se guarda localmente

## 🆘 Comandos útiles

```python
# Ver quién eres
whoami()

# Ver tus submissions anteriores
get_submissions()

# Ver submissions de un challenge específico
get_submissions(challenge_id=35)

# Cerrar sesión (borra token local)
logout()

# Testear conexión
test_connection()
```

## 📊 Ejemplo completo desde cero

```python
# 1. Importar
from grader_qiskit_client import *

# 2. Login simple (solo username)
login('MiNombre_UAM')

# 3. Ver el challenge
challenges = get_challenge(35)
print(challenges)

# 4. Trabajar en el notebook...
# (ejecutar Halloween35.ipynb)

# 5. Enviar (ejemplo simplificado)
mi_codigo = """
alpha_vqe_result = mi_resultado_vqe_alpha
beta_vqe_result = mi_resultado_vqe_beta
alpha_gap_ev = 4.5
beta_gap_ev = 2.3
alpha_homo_lumo = 0.165
beta_homo_lumo = 0.085
"""

submit(35, mi_codigo)

# 6. Ver ranking
show_leaderboard(10)  # Top 10

# 7. Ver mi progreso
show_progress()
```

## 🎃 ¡Eso es todo!

No necesitas:
- ❌ Registrarte previamente
- ❌ Proporcionar email
- ❌ Crear contraseña compleja
- ❌ Confirmar cuenta

Solo necesitas:
- ✅ Elegir un username
- ✅ Hacer `login('tu_username')`
- ✅ Empezar a enviar código

Happy Halloween Coding! 👻
