# 🎃 Halloween Qiskit Challenge 2025

Welcome to the **Halloween Qiskit Challenge**! A quantum computing competition where you'll solve quantum chemistry mysteries using Qiskit.

## 🎯 What is This?

This is Challenge 35: **"A Halloween Carol"** - A quantum chemistry challenge where you analyze two mysterious molecules (Alpha and Beta) using:
- **VQE (Variational Quantum Eigensolver)** to find ground state energies
- **HOMO-LUMO Gap Analysis** to determine molecular reactivity
- **Quantum State Divergence** to compare quantum states

## 🚀 Quick Start

### 1. Download the Client

Download `grader_qiskit_client.py` from the repository:
```bash
curl -O https://raw.githubusercontent.com/5ansus/graderServer/main/grader_qiskit_client.py
```

### 2. Login (Auto-Registration)

No need to register! Just pick a username:

```python
from grader_qiskit_client import login

# Login (creates account automatically if it doesn't exist)
login('your_username')
```

### 3. Solve the Challenge Locally

Work on the challenge in your Jupyter notebook (`Halloween35.ipynb`). Use Qiskit to:
- Calculate VQE ground state energies for Alpha and Beta molecules
- Compute HOMO-LUMO gaps
- Perform quantum state analysis

### 4. Submit Your Results

**Don't send code!** Just send your calculated results:

```python
from grader_qiskit_client import submit_results

submit_results(
    35,
    alpha_vqe_result=-2.1847,      # Your Alpha VQE energy
    beta_vqe_result=0.9375,        # Your Beta VQE energy
    alpha_gap_ev=33.57,            # Alpha HOMO-LUMO gap in eV
    beta_gap_ev=27.21,             # Beta HOMO-LUMO gap in eV
    alpha_homo_lumo=1.234,         # Alpha gap in Hartree
    beta_homo_lumo=1.0             # Beta gap in Hartree
)
```

### 5. Get Instant Feedback

```
✅ Score: 85/100
Feedback:
✅ Task 1 (VQE): Excellent! Very accurate energies.
✅ Task 2 (HOMO-LUMO): Perfect! Alpha gap: 33.57 eV, Beta gap: 27.21 eV
   💡 Beta is more reactive than Alpha (smaller gap)
⚠️ Task 3 (QSD): Values present but missing data for verification.

📚 You need ≥70 points to pass. You have 85/100.
```

## 📊 Scoring System

**Total: 100 points** (need ≥70 to pass)

### Task 1: VQE Analysis (30 points)
- **30 pts**: Energies within ±0.1 Hartree of reference values
- **20 pts**: Within ±0.5 Hartree
- **10 pts**: Any reasonable quantum chemistry values

**Reference values (approximate)**:
- Alpha: ~-2.18 Hartree
- Beta: ~0.94 Hartree

### Task 2: HOMO-LUMO Gap (30 points)
- **30 pts**: Correct gaps in eV (0-15 range) + correct interpretation
- **15 pts**: Gaps calculated but unusual values

**Hint**: The molecule with the **smaller gap** is more reactive!

### Task 3: Quantum State Divergence (40 points)
- **40 pts**: Complete analysis with consistent units (eV ↔ Hartree)
- **25 pts**: Values present but unit inconsistencies
- **20 pts**: Partial analysis

**Conversion**: 1 Hartree = 27.211 eV

## 🏆 Leaderboard & Progress

Check your ranking:

```python
from grader_qiskit_client import get_leaderboard, get_progress

# View top participants
get_leaderboard()

# Check your personal progress
get_progress()
```

## 💡 Tips & Tricks

### 1. Run Everything Locally
- Use your own machine's power
- Debug and visualize as needed
- No server timeouts!

### 2. Unit Consistency is Key
Make sure your gap values match:
```python
# If alpha_gap_ev = 33.57 eV, then:
alpha_homo_lumo = 33.57 / 27.211  # = 1.234 Hartree
```

### 3. Check Reasonableness
- VQE energies should be negative for bound states
- HOMO-LUMO gaps typically 0-10 eV for most molecules
- Smaller gap = more reactive molecule

### 4. Unlimited Attempts
- Submit as many times as you want
- Only your **best score** counts
- Use feedback to improve!

## 🔧 Complete Example

```python
from grader_qiskit_client import login, submit_results, get_leaderboard
from AHC25Data import get_alpha_hamiltonian, get_beta_hamiltonian
from qiskit_algorithms import VQE
from qiskit.primitives import Estimator
from qiskit.circuit.library import TwoLocal

# 1. Login
login('alice_quantum')

# 2. Get Hamiltonians
alpha_ham = get_alpha_hamiltonian()
beta_ham = get_beta_hamiltonian()

# 3. Run VQE (example with statevector simulator)
ansatz = TwoLocal(4, rotation_blocks='ry', entanglement_blocks='cx', reps=3)
estimator = Estimator()

# Alpha VQE
alpha_vqe = VQE(estimator, ansatz)
alpha_result = alpha_vqe.compute_minimum_eigenvalue(alpha_ham)
alpha_vqe_result = alpha_result.eigenvalue

# Beta VQE
beta_vqe = VQE(estimator, ansatz)
beta_result = beta_vqe.compute_minimum_eigenvalue(beta_ham)
beta_vqe_result = beta_result.eigenvalue

# 4. Calculate HOMO-LUMO gaps (example - you need to implement this)
# Use exact diagonalization or your VQE results
alpha_homo_lumo = 1.234  # in Hartree
beta_homo_lumo = 1.0     # in Hartree

alpha_gap_ev = alpha_homo_lumo * 27.211  # Convert to eV
beta_gap_ev = beta_homo_lumo * 27.211

# 5. Submit results
submit_results(
    35,
    alpha_vqe_result=float(alpha_vqe_result),
    beta_vqe_result=float(beta_vqe_result),
    alpha_gap_ev=alpha_gap_ev,
    beta_gap_ev=beta_gap_ev,
    alpha_homo_lumo=alpha_homo_lumo,
    beta_homo_lumo=beta_homo_lumo
)

# 6. Check leaderboard
get_leaderboard()
```

## 🌐 API Endpoints

- **Base URL**: `https://uamcpra.pythonanywhere.com/api/`
- **Homepage**: `https://uamcpra.pythonanywhere.com/`
- **Admin Panel**: `https://uamcpra.pythonanywhere.com/admin/`

### Main Endpoints
- `POST /api/login` - Login (auto-creates user)
- `GET /api/challenges` - List challenges
- `POST /api/submit-results` - Submit results (recommended)
- `POST /api/submit` - Submit code (legacy, not recommended)
- `GET /api/leaderboard` - View rankings
- `GET /api/progress` - Your progress

## ❓ FAQ

### Q: Do I need to register first?
**A**: No! Just use `login('your_username')` and your account is created automatically.

### Q: Can I submit multiple times?
**A**: Yes! Submit as many times as you want. Only your best score counts.

### Q: Why submit results instead of code?
**A**: It's faster, lighter, and lets you run heavy computations on your own machine without server limitations.

### Q: What if I get an error?
**A**: Check:
1. You're sending all 6 required variables
2. Values are reasonable (VQE energies negative, gaps positive)
3. Units are consistent (eV ↔ Hartree conversion)

### Q: How do I see my rank?
**A**: Use `get_leaderboard()` or check the web interface at https://uamcpra.pythonanywhere.com/

### Q: Can I see others' solutions?
**A**: No, submissions are private. But you can compete on the leaderboard!

## 📚 Resources

- **Repository**: https://github.com/5ansus/graderServer
- **Qiskit Documentation**: https://qiskit.org/documentation/
- **Qiskit Algorithms**: https://qiskit.org/ecosystem/algorithms/
- **Challenge Data**: Use `AHC25Data.py` (provided in notebook)

## 🎓 Learning Resources

### Variational Quantum Eigensolver (VQE)
- [Qiskit VQE Tutorial](https://qiskit.org/textbook/ch-algorithms/vqe.html)
- VQE finds the ground state energy of a molecule

### HOMO-LUMO Gap
- **HOMO**: Highest Occupied Molecular Orbital
- **LUMO**: Lowest Unoccupied Molecular Orbital
- **Gap**: Energy difference (small gap = reactive molecule)

### Quantum State Divergence
- Compares how different two quantum states are
- Uses fidelity measures and subspace projections

## 🤝 Support

Having issues? Check:
1. **Client version**: Make sure you have the latest `grader_qiskit_client.py`
2. **Dependencies**: `pip install qiskit qiskit-algorithms requests`
3. **Token**: If authentication fails, try logging in again

## 🎃 Good Luck!

May the quantum odds be ever in your favor!

Remember:
- 🧪 Science is about trying and learning
- 🎯 Aim for understanding, not just points
- 🤝 Share knowledge (but not solutions!)
- 🏆 Compete fairly and have fun!

**Happy Halloween Hacking! 👻🔬⚛️**

---

*Halloween Qiskit Challenge 2025 - MadQFF'25*
*Made with ❤️ for the quantum computing community*
