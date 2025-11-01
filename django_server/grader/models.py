from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils import timezone


class Challenge(models.Model):
    """
    Modelo para los challenges/ejercicios.
    Puedes añadir nuevos challenges fácilmente desde el admin de Django.
    """
    id = models.IntegerField(primary_key=True)  # Para mantener IDs específicos (1-5)
    name = models.CharField(max_length=200)
    description = models.TextField()
    max_score = models.IntegerField(default=100)
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # Campo para el código de evaluación o test cases
    evaluation_code = models.TextField(
        blank=True,
        help_text="Código Python para evaluar las submissions de este challenge"
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Challenge'
        verbose_name_plural = 'Challenges'

    def __str__(self):
        return f"Challenge {self.id}: {self.name}"

    def get_completion_rate(self):
        """Calcula el porcentaje de usuarios que completaron este challenge"""
        total_users = User.objects.count()
        if total_users == 0:
            return 0
        completed = Submission.objects.filter(
            challenge=self,
            passed=True
        ).values('user').distinct().count()
        return (completed / total_users) * 100


class UserProfile(models.Model):
    """
    Extensión del modelo User para guardar información adicional del usuario.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"Profile of {self.user.username}"

    def update_total_score(self):
        """Actualiza el score total del usuario basado en sus mejores submissions"""
        best_scores = Submission.objects.filter(
            user=self.user
        ).values('challenge').annotate(
            best_score=Max('score')
        )

        self.total_score = sum(item['best_score'] for item in best_scores)
        self.save()
        return self.total_score

    def get_challenges_completed(self):
        """Retorna el número de challenges completados (pasados)"""
        return Submission.objects.filter(
            user=self.user,
            passed=True
        ).values('challenge').distinct().count()

    def get_rank(self):
        """Obtiene la posición del usuario en el ranking"""
        higher_scores = UserProfile.objects.filter(
            total_score__gt=self.total_score
        ).count()
        return higher_scores + 1


class Submission(models.Model):
    """
    Modelo para guardar todas las submissions de los usuarios.
    Cada vez que un usuario envía código, se guarda aquí.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='submissions')
    code = models.TextField()
    score = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    # Información adicional
    execution_time = models.FloatField(null=True, blank=True, help_text="Tiempo de ejecución en segundos")
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        indexes = [
            models.Index(fields=['user', 'challenge']),
            models.Index(fields=['challenge', 'passed']),
            models.Index(fields=['-submitted_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - Challenge {self.challenge.id} - Score: {self.score}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar el score total del usuario después de cada submission
        if hasattr(self.user, 'profile'):
            self.user.profile.update_total_score()

    def is_best_score(self):
        """Verifica si esta submission es el mejor score del usuario para este challenge"""
        best = Submission.objects.filter(
            user=self.user,
            challenge=self.challenge
        ).aggregate(Max('score'))
        return self.score == best['score__max']


# Signals para crear automáticamente UserProfile cuando se crea un User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Leaderboard(models.Model):
    """
    Modelo para el leaderboard/ranking de usuarios.
    Inspirado en old_requirements.py - guarda puntuación agregada.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard', primary_key=True)
    total_score = models.IntegerField(default=0)
    challenges_completed = models.IntegerField(default=0)  # Número de challenges pasados
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_score', '-challenges_completed', 'last_updated']
        verbose_name = 'Leaderboard Entry'
        verbose_name_plural = 'Leaderboard'

    def __str__(self):
        return f"{self.user.username}: {self.total_score} points, {self.challenges_completed} completed"

    def get_rank(self):
        """Obtiene la posición del usuario en el ranking"""
        higher_scores = Leaderboard.objects.filter(
            total_score__gt=self.total_score
        ).count()
        return higher_scores + 1


# Signal para crear Leaderboard cuando se crea un User
@receiver(post_save, sender=User)
def create_user_leaderboard(sender, instance, created, **kwargs):
    if created:
        Leaderboard.objects.get_or_create(user=instance)
