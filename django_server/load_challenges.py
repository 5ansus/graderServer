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
        'id': 1,
        'name': 'Challenge 1: Introducción',
        'description': 'Primer desafío básico',
        'max_score': 100,
        'difficulty': 'easy',
        'is_active': True,
    },
    {
        'id': 2,
        'name': 'Challenge 2: Intermedio',
        'description': 'Segundo desafío de dificultad media',
        'max_score': 100,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 3,
        'name': 'Challenge 3: Avanzado',
        'description': 'Tercer desafío más complejo',
        'max_score': 100,
        'difficulty': 'medium',
        'is_active': True,
    },
    {
        'id': 4,
        'name': 'Challenge 4: Experto',
        'description': 'Cuarto desafío de nivel experto',
        'max_score': 100,
        'difficulty': 'hard',
        'is_active': True,
    },
    {
        'id': 5,
        'name': 'Challenge 5: Maestro',
        'description': 'Quinto desafío del nivel maestro',
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
