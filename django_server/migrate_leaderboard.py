"""
Script para migrar datos al nuevo modelo Leaderboard y actualizar puntuaciones.

Este script:
1. Crea entradas de Leaderboard para todos los usuarios existentes
2. Recalcula las puntuaciones basándose en las submissions pasadas
3. Actualiza los puntajes de challenges a 20 puntos cada uno

Ejecutar con: python migrate_leaderboard.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'halloween_server.settings')
django.setup()

from django.contrib.auth.models import User
from grader.models import Challenge, Submission, Leaderboard

def migrate_leaderboard():
    print("🎃 Iniciando migración del Leaderboard...\n")

    # Paso 1: Crear entradas de Leaderboard para todos los usuarios
    print("Paso 1: Creando entradas de Leaderboard...")
    users = User.objects.all()
    for user in users:
        leaderboard, created = Leaderboard.objects.get_or_create(user=user)
        if created:
            print(f"  ✅ Creada entrada para {user.username}")
        else:
            print(f"  ℹ️  Entrada ya existente para {user.username}")

    print(f"\nTotal usuarios procesados: {users.count()}\n")

    # Paso 2: Recalcular puntuaciones basándose en submissions pasadas
    print("Paso 2: Recalculando puntuaciones...")
    for user in users:
        leaderboard = Leaderboard.objects.get(user=user)

        # Obtener todos los challenges que el usuario ha pasado
        passed_challenges = Submission.objects.filter(
            user=user,
            passed=True
        ).values('challenge').distinct()

        # Contar challenges completados
        challenges_completed = passed_challenges.count()

        # Calcular score total (20 puntos por challenge pasado)
        total_score = challenges_completed * 20

        # Actualizar leaderboard
        leaderboard.total_score = total_score
        leaderboard.challenges_completed = challenges_completed
        leaderboard.save()

        if challenges_completed > 0:
            print(f"  📊 {user.username}: {total_score} puntos, {challenges_completed} tasks completadas")

    print("\n✨ Migración completada!")

    # Paso 3: Mostrar ranking
    print("\n🏆 RANKING ACTUAL:")
    print("-" * 60)
    leaderboard_entries = Leaderboard.objects.all().order_by(
        '-total_score', '-challenges_completed', 'last_updated'
    )[:10]

    for idx, entry in enumerate(leaderboard_entries, start=1):
        print(f"  {idx}. {entry.user.username:20s} | {entry.total_score:3d} puntos | {entry.challenges_completed} tasks")

    print("-" * 60)
    print(f"\nTotal participantes: {Leaderboard.objects.count()}")
    print(f"Usuarios con al menos 1 task: {Leaderboard.objects.filter(challenges_completed__gt=0).count()}")
    print(f"Usuarios con todas las tasks (100 pts): {Leaderboard.objects.filter(total_score=100).count()}")

if __name__ == '__main__':
    migrate_leaderboard()
