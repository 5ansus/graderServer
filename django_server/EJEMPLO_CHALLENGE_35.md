# 🎃 Ejemplo de Submission para Challenge 35

## Cómo enviar tu solución del Halloween Challenge

### Opción 1: Enviar todas las variables del notebook

```python
from grader_qiskit_client import submit

# Después de ejecutar TODO el notebook Halloween35.ipynb, envía las variables clave:

submission_code = '''
# Resultados de VQE (Task 1)
alpha_vqe_result = <tu resultado de VQE para Alpha>
beta_vqe_result = <tu resultado de VQE para Beta>

# Resultados de HOMO-LUMO (Task 2)
alpha_gap_ev = <tu gap en eV para Alpha>
beta_gap_ev = <tu gap en eV para Beta>
alpha_homo_lumo = <tu gap en Hartree para Alpha>
beta_homo_lumo = <tu gap en Hartree para Beta>

# Resultados de QSD (Task 3 - opcional para bonus)
V_alpha = <tu matriz de Krylov para Alpha>
V_beta = <tu matriz de Krylov para Beta>
evals_alpha = <tus eigenvalores para Alpha>
evals_beta = <tus eigenvalores para Beta>
fidelity_matrix = <tu matriz de fidelidad>
'''

# Enviar
submit(35, submission_code)
```

### Opción 2: Enviar código ejecutable completo

Si prefieres, puedes enviar el código completo de las secciones que completaste:

```python
from grader_qiskit_client import submit

submission_code = '''
# Importar todo lo necesario
import numpy as np
from qiskit import QuantumCircuit
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit.primitives import StatevectorEstimator as Estimator
from qiskit.circuit.library import EfficientSU2

# Obtener Hamiltonianos (asumiendo que ya están definidos)
# alpha_ham = get_alpha_hamiltonian()
# beta_ham = get_beta_hamiltonian()

# Task 1: VQE
def run_vqe(hamiltonian):
    num_qubits = hamiltonian.num_qubits
    ansatz = EfficientSU2(num_qubits, reps=3, entanglement='linear')
    optimizer = SLSQP(maxiter=300, ftol=1e-8)
    estimator = Estimator()

    vqe = VQE(estimator, ansatz, optimizer)
    result = vqe.compute_minimum_eigenvalue(hamiltonian)
    return result

alpha_vqe_result = run_vqe(alpha_ham)
beta_vqe_result = run_vqe(beta_ham)

# Task 2: HOMO-LUMO Gap
def homo_lumo_analysis(eigenvalues):
    homo = eigenvalues[0]
    lumo = eigenvalues[1]
    gap = lumo - homo
    gap_ev = gap * 27.2114
    return gap, gap_ev

alpha_homo_lumo, alpha_gap_ev = homo_lumo_analysis(alpha_exact_evals)
beta_homo_lumo, beta_gap_ev = homo_lumo_analysis(beta_exact_evals)

# Task 3: QSD (implementación completa)
# ... tu código de QSD aquí ...
'''

submit(35, submission_code)
```

## 📊 Sistema de Puntuación

### Task 1: VQE Analysis (30 puntos)
- ✅ Resultados VQE correctos para Alpha y Beta
- ✅ Energías en rango razonable (-10 < E < 0 Hartree)

### Task 2: HOMO-LUMO Gap (30 puntos)
- ✅ Cálculo correcto de gaps en eV
- ✅ Valores razonables (0-15 eV)
- 💡 Bonus: Interpretación correcta (Beta más reactivo)

### Task 3: QSD Analysis (40 puntos)
- ✅ Construcción de subespacio de Krylov
- ✅ Proyección QSD correcta
- ✅ Matriz de fidelidad calculada
- 💡 Bonus: Identificación de estados correlacionados

## ✅ Pasar el Challenge

- **70+ puntos**: Challenge completado ✓
- **90+ puntos**: Excelencia 🌟

## 🔍 Ejemplo Simplificado

Si solo quieres probar el sistema de grading:

```python
from grader_qiskit_client import submit

# Ejemplo con valores ficticios (NO pasará, solo para testing)
test_code = '''
# Valores de prueba
alpha_vqe_result = type('obj', (object,), {'eigenvalue': -2.5})()
beta_vqe_result = type('obj', (object,), {'eigenvalue': -1.8})()
alpha_gap_ev = 4.5
beta_gap_ev = 2.3
alpha_homo_lumo = 0.165
beta_homo_lumo = 0.085
'''

submit(35, test_code)
```

## 💡 Tips

1. **Ejecuta TODO el notebook** antes de enviar
2. **Verifica que las variables existen** en tu namespace
3. **Los resultados deben ser objetos Python válidos** (no solo prints)
4. **Task 3 es opcional** pero da muchos puntos
5. **Puedes enviar múltiples veces** - solo cuenta el mejor score

## 🆘 Si tienes problemas

```python
from grader_qiskit_client import *

# Ver el challenge
challenges = get_challenge(35)
print(challenges)

# Ver tus submissions anteriores
my_submissions = get_submissions(challenge_id=35)
print(my_submissions)

# Ver tu progreso
show_progress()
```

## 🎃 Happy Halloween Coding!
