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
        'id': 35,
        'name': 'A Halloween Carol: Quantum Chemistry Mystery',
        'description': '''Analyze two mysterious substances (Alpha and Beta) from a haunted laboratory using quantum chemistry techniques.

Your mission involves three tasks:
1. Use VQE to find ground state energies
2. Calculate HOMO-LUMO gaps to determine reactivity
3. Apply QSD with Krylov subspace to discover hidden relationships

Complete the quantum chemistry analysis to uncover the truth behind these substances.''',
        'max_score': 100,
        'difficulty': 'hard',
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
