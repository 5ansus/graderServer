"""
Script para cargar los challenges iniciales en la base de datos.

Ejecutar con: python load_challenges.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'halloween_server.settings')
django.setup()

from grader.models import Challenge

challenges_data = [
    {
        'id': 351,
        'name': 'Challenge 35 - Task 1: VQE Analysis',
        'description': 'Use VQE to find ground state energies for Alpha and Beta molecules.',
        'max_score': 20,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 352,
        'name': 'Challenge 35 - Task 2: HOMO-LUMO Gap',
        'description': 'Calculate HOMO-LUMO gaps to determine reactivity.',
        'max_score': 20,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 353,
        'name': 'Challenge 35 - Task 3: QSD Analysis',
        'description': 'Apply QSD with Krylov subspace to discover hidden relationships.',
        'max_score': 20,
        'difficulty': 'hard',
        'is_active': True,
    },
    {
        'id': 354,
        'name': 'Challenge 35 - Task 4: Final Energy Beta',
        'description': 'Calculate final energy for Beta molecule.',
        'max_score': 20,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 355,
        'name': 'Challenge 35 - Task 5: Final Energy Perturbed',
        'description': 'Calculate final energy for perturbed system.',
        'max_score': 20,
        'difficulty': 'medium',
        'is_active': True,
    },
    # New: Challenge 36 tasks (361-363)
    {
        'id': 361,
        'name': 'Challenge 36 - Task 1: Classification Accuracy (361)',
        'description': 'Evaluate predictions against hidden labels; require >=98% accuracy.',
        'max_score': 20,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 362,
        'name': 'Challenge 36 - Task 2: Image Generation (362)',
        'description': 'Generated images',
        'max_score': 20,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 363,
        'name': 'Challenge 36 - Task 3: Reinforcement Rewards (363)',
        'description': 'Total rewards',
        'max_score': 20,
        'difficulty': 'easy',
        'is_active': True,
    },
    # Challenge 37 tasks (371-378)
    {
        'id': 371,
        'name': 'Challenge 37 - Task 1.1: Bell State Creation (371)',
        'description': 'Create a Bell pair circuit and measure Bell outcomes.',
        'max_score': 10,
        'difficulty': 'easy',
        'is_active': True,
    },
    {
        'id': 372,
        'name': 'Challenge 37 - Task 1.2: Noise Model Creation (372)',
        'description': 'Create a bit-flip noise model and demonstrate its effect.',
        'max_score': 10,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 373,
        'name': 'Challenge 37 - Task 1.3: Fidelity vs Noise (373)',
        'description': 'Function that computes fidelity for several noise levels.',
        'max_score': 15,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 374,
        'name': 'Challenge 37 - Task 2.1: Three-Qubit Encoding (374)',
        'description': 'Encode one logical qubit into three physical qubits.',
        'max_score': 15,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 375,
        'name': 'Challenge 37 - Task 2.2: Syndrome Measurement (375)',
        'description': 'Implement syndrome measurement for three-qubit code.',
        'max_score': 15,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 376,
        'name': 'Challenge 37 - Task 3.2: Error Correction Effectiveness (376)',
        'description': 'Compare protected vs unprotected pipelines under noise.',
        'max_score': 20,
        'difficulty': 'hard',
        'is_active': True,
    },
    {
        'id': 377,
        'name': 'Challenge 37 - Task 4.1: Shor Code Encoding (377)',
        'description': 'Implement Shor code encoding for one logical qubit.',
        'max_score': 10,
        'difficulty': 'hard',
        'is_active': True,
    },
    {
        'id': 378,
        'name': 'Challenge 37 - Task 4.2: Shor Syndrome Measurement (378)',
        'description': 'Measure syndromes for the Shor code (X-type).',
        'max_score': 5,
        'difficulty': 'medium',
        'is_active': True,
    },
]

print("Cargando challenges...")

for ch_data in challenges_data:
    challenge, created = Challenge.objects.update_or_create(
        id=ch_data['id'],
        defaults={
            'name': ch_data['name'],
            'description': ch_data['description'],
            'max_score': ch_data['max_score'],
            'difficulty': ch_data['difficulty'],
            'is_active': ch_data['is_active'],
        }
    )

    if created:
        print(f"✅ Challenge {challenge.id} creado: {challenge.name}")
    else:
        print(f"🔄 Challenge {challenge.id} actualizado: {challenge.name}")

print(f"\n✨ Total de challenges: {Challenge.objects.count()}")
print("¡Listo! Ahora puedes añadir más challenges desde el admin de Django.")
