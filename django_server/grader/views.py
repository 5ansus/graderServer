from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Max, Count, Q
from django.shortcuts import render
from .models import Challenge, Submission, UserProfile
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    ChallengeSerializer, SubmissionSerializer, SubmitCodeSerializer,
    LeaderboardSerializer, ProgressSerializer
)
from .evaluators import CodeEvaluator


# ==================== INDEX / HOME ====================

class IndexView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Vista principal de la API"""
        total_users = User.objects.count()
        total_challenges = Challenge.objects.filter(is_active=True).count()
        total_submissions = Submission.objects.count()

        # Si se solicita HTML (navegador), renderizar template
        if 'text/html' in request.headers.get('Accept', ''):
            context = {
                'stats': {
                    'total_users': total_users,
                    'total_challenges': total_challenges,
                    'total_submissions': total_submissions,
                }
            }
            return render(request, 'index.html', context)

        # Si se solicita JSON (API), devolver JSON
        data = {
            'message': '🎃 Halloween Qiskit Challenge API',
            'version': '1.0',
            'status': 'online',
            'endpoints': {
                'authentication': {
                    'register': '/api/register',
                    'login': '/api/login',
                    'profile': '/api/profile (requires authentication)',
                },
                'challenges': {
                    'list': '/api/challenges (requires authentication)',
                    'detail': '/api/challenges/<id> (requires authentication)',
                },
                'submissions': {
                    'submit': '/api/submit (requires authentication)',
                    'list': '/api/submissions (requires authentication)',
                    'detail': '/api/submissions/<id> (requires authentication)',
                },
                'leaderboard': {
                    'leaderboard': '/api/leaderboard (requires authentication)',
                    'progress': '/api/progress (requires authentication)',
                    'stats': '/api/stats (requires authentication)',
                },
                'health': '/api/health',
                'admin': '/admin/',
            },
            'stats': {
                'total_users': total_users,
                'total_challenges': total_challenges,
                'total_submissions': total_submissions,
            },
            'documentation': 'https://github.com/5ansus/graderServer',
            'client': 'Use grader_qiskit_client.py to interact with this API',
        }

        return Response(data)
# ==================== AUTENTICACIÓN ====================

class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'Registration successful',
                'token': token.key,
                'username': user.username
            }, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Si no se proporciona password, usar el username como password por defecto
        if not password:
            password = username

        # Intentar autenticar
        user = authenticate(username=username, password=password)

        # Si el usuario no existe, crearlo automáticamente
        if not user:
            try:
                user = User.objects.get(username=username)
                # Usuario existe pero password incorrecta
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except User.DoesNotExist:
                # Usuario no existe, crearlo
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=f'{username}@halloweenchallenge.local'
                )
                message = f'Welcome {username}! User created successfully'
        else:
            message = 'Login successful'

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'message': message,
            'token': token.key,
            'username': user.username
        }, status=status.HTTP_200_OK)


class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data})


# ==================== CHALLENGES ====================

class ChallengeListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        return Challenge.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'challenges': serializer.data})


class ChallengeDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'challenge': serializer.data})


# ==================== SUBMISSIONS ====================

class SubmitCodeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubmitCodeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        challenge_id = serializer.validated_data['challenge_id']
        code = serializer.validated_data['code']

        try:
            challenge = Challenge.objects.get(id=challenge_id, is_active=True)
        except Challenge.DoesNotExist:
            return Response(
                {'error': 'Challenge not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Evaluar el código
        score, passed, feedback, execution_time = CodeEvaluator.evaluate(challenge_id, code)

        # Guardar la submission
        submission = Submission.objects.create(
            user=request.user,
            challenge=challenge,
            code=code,
            score=score,
            passed=passed,
            feedback=feedback,
            execution_time=execution_time
        )

        return Response({
            'submission_id': submission.id,
            'score': score,
            'max_score': challenge.max_score,
            'passed': passed,
            'feedback': feedback,
            'execution_time': round(execution_time, 3)
        }, status=status.HTTP_200_OK)


class SubmissionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        queryset = Submission.objects.filter(user=self.request.user)

        challenge_id = self.request.query_params.get('challenge_id')
        if challenge_id:
            queryset = queryset.filter(challenge_id=challenge_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'submissions': serializer.data})


class SubmissionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'submission': serializer.data})


# ==================== LEADERBOARD Y ESTADÍSTICAS ====================

class LeaderboardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get('limit', 50))

        # Obtener usuarios ordenados por score
        profiles = UserProfile.objects.select_related('user').order_by('-total_score')

        leaderboard_data = []
        user_position = None

        for idx, profile in enumerate(profiles, start=1):
            data = {
                'username': profile.user.username,
                'total_score': profile.total_score,
                'challenges_completed': profile.get_challenges_completed(),
                'rank': idx
            }

            if idx <= limit:
                leaderboard_data.append(data)

            if profile.user == request.user:
                user_position = idx

        return Response({
            'leaderboard': leaderboard_data,
            'user_position': user_position
        })


class ProgressView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = user.profile

        total_challenges = Challenge.objects.filter(is_active=True).count()
        challenges_completed = profile.get_challenges_completed()
        total_submissions = Submission.objects.filter(user=user).count()
        rank = profile.get_rank()

        return Response({
            'total_score': profile.total_score,
            'challenges_completed': challenges_completed,
            'total_challenges': total_challenges,
            'total_submissions': total_submissions,
            'rank': rank
        })


class StatsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_users = User.objects.count()
        total_challenges = Challenge.objects.filter(is_active=True).count()
        total_submissions = Submission.objects.count()

        return Response({
            'total_users': total_users,
            'total_challenges': total_challenges,
            'total_submissions': total_submissions
        })


# ==================== HEALTH CHECK ====================

class HealthCheckView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'API is running'
        }, status=status.HTTP_200_OK)
