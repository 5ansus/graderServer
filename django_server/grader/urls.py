from django.urls import path
from .views import (
    HomeView, APIIndexView,
    RegisterView, LoginView, ProfileView,
    ChallengeListView, ChallengeDetailView,
    SubmitCodeView, SubmitResultsView, SubmissionListView, SubmissionDetailView,
    LeaderboardView, ProgressView, StatsView,
    DownloadClientView,
    HealthCheckView
)

urlpatterns = [
    # Home (raíz del sitio)
    path('', HomeView.as_view(), name='home'),

    # API Index / Documentation
    path('api/', APIIndexView.as_view(), name='api-index'),

    # Autenticación
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/login', LoginView.as_view(), name='login'),
    path('api/profile', ProfileView.as_view(), name='profile'),

    # Challenges
    path('api/challenges', ChallengeListView.as_view(), name='challenges'),
    path('api/challenges/<int:pk>', ChallengeDetailView.as_view(), name='challenge-detail'),

    # Submissions
    path('api/submit', SubmitCodeView.as_view(), name='submit'),
    path('api/submit-results', SubmitResultsView.as_view(), name='submit-results'),
    path('api/submissions', SubmissionListView.as_view(), name='submissions'),
    path('api/submissions/<int:pk>', SubmissionDetailView.as_view(), name='submission-detail'),

    # Leaderboard y estadísticas
    path('api/leaderboard', LeaderboardView.as_view(), name='leaderboard'),
    path('api/progress', ProgressView.as_view(), name='progress'),
    path('api/stats', StatsView.as_view(), name='stats'),

    # Client download
    path('api/download-client', DownloadClientView.as_view(), name='download-client'),

    # Health check
    path('api/health', HealthCheckView.as_view(), name='health'),
]
