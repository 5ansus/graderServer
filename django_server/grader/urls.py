from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    ChallengeListView, ChallengeDetailView,
    SubmitCodeView, SubmissionListView, SubmissionDetailView,
    LeaderboardView, ProgressView, StatsView,
    HealthCheckView
)

urlpatterns = [
    # Autenticación
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),

    # Challenges
    path('challenges', ChallengeListView.as_view(), name='challenges'),
    path('challenges/<int:pk>', ChallengeDetailView.as_view(), name='challenge-detail'),

    # Submissions
    path('submit', SubmitCodeView.as_view(), name='submit'),
    path('submissions', SubmissionListView.as_view(), name='submissions'),
    path('submissions/<int:pk>', SubmissionDetailView.as_view(), name='submission-detail'),

    # Leaderboard y estadísticas
    path('leaderboard', LeaderboardView.as_view(), name='leaderboard'),
    path('progress', ProgressView.as_view(), name='progress'),
    path('stats', StatsView.as_view(), name='stats'),

    # Health check
    path('health', HealthCheckView.as_view(), name='health'),
]
