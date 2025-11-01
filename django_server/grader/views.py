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
    SubmitResultsSerializer, LeaderboardSerializer, ProgressSerializer
)
from .evaluators import CodeEvaluator


# ==================== HOME / INDEX ====================

class HomeView(views.APIView):
    """Vista principal del sitio (raíz)"""
    permission_classes = [AllowAny]

    def get(self, request):
        total_users = User.objects.count()
        total_challenges = Challenge.objects.filter(is_active=True).count()
        total_submissions = Submission.objects.count()

        context = {
            'stats': {
                'total_users': total_users,
                'total_challenges': total_challenges,
                'total_submissions': total_submissions,
            }
        }
        return render(request, 'home.html', context)


class APIIndexView(views.APIView):
    """Vista de documentación de la API (/api/)"""
    permission_classes = [AllowAny]

    def get(self, request):
        """Main API view"""
        total_users = User.objects.count()
        total_challenges = Challenge.objects.filter(is_active=True).count()
        total_submissions = Submission.objects.count()

        # If HTML is requested (browser), render template
        if 'text/html' in request.headers.get('Accept', ''):
            context = {
                'stats': {
                    'total_users': total_users,
                    'total_challenges': total_challenges,
                    'total_submissions': total_submissions,
                }
            }
            return render(request, 'index.html', context)

        # If JSON is requested (API), return JSON
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
                    'submit-results': '/api/submit-results (requires authentication)',
                    'list': '/api/submissions (requires authentication)',
                    'detail': '/api/submissions/<id> (requires authentication)',
                },
                'leaderboard': {
                    'leaderboard': '/api/leaderboard (PUBLIC - no authentication required)',
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
            'leaderboard_url': '/api/leaderboard',
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


class SubmitResultsView(views.APIView):
    """
    Endpoint ligero: solo recibe resultados finales, sin ejecutar código.
    Ideal para challenges pesados donde el usuario ejecuta localmente.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubmitResultsSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        challenge_id = serializer.validated_data['challenge_id']
        results = serializer.validated_data['results']

        try:
            challenge = Challenge.objects.get(id=challenge_id, is_active=True)
        except Challenge.DoesNotExist:
            return Response(
                {'error': 'Challenge not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Evaluar los resultados (sin ejecutar código)
        # Challenge 351-355 son tasks individuales de Challenge 35
        # Pasar max_score dinámicamente desde el challenge
        if challenge_id == 351:
            score, passed, feedback, execution_time = CodeEvaluator.evaluate_challenge_35_task1(results, challenge.max_score)
        elif challenge_id == 352:
            score, passed, feedback, execution_time = CodeEvaluator.evaluate_challenge_35_task2(results, challenge.max_score)
        elif challenge_id == 353:
            score, passed, feedback, execution_time = CodeEvaluator.evaluate_challenge_35_task3(results, challenge.max_score)
        elif challenge_id == 354:
            score, passed, feedback, execution_time = CodeEvaluator.evaluate_challenge_35_task4(results, challenge.max_score)
        elif challenge_id == 355:
            score, passed, feedback, execution_time = CodeEvaluator.evaluate_challenge_35_task5(results, challenge.max_score)
        elif challenge_id == 361:
            score, passed, feedback, execution_time = CodeEvaluator.evaluate_challenge_36_task1(results, challenge.max_score)
        elif challenge_id == 362:
            score, passed, feedback, execution_time = CodeEvaluator.evaluate_challenge_36_task2(results, challenge.max_score)
        elif challenge_id == 363:
            score, passed, feedback, execution_time = CodeEvaluator.evaluate_challenge_36_task3(results, challenge.max_score)
        elif challenge_id == 35:
            score, passed, feedback, execution_time = CodeEvaluator.evaluate_challenge_35_results(results)
        else:
            return Response(
                {'error': 'This challenge does not support results-only submission'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Guardar la submission (con código vacío o JSON de resultados)
        import json
        submission = Submission.objects.create(
            user=request.user,
            challenge=challenge,
            code=f"# Results submission\n{json.dumps(results, indent=2)}",
            score=score,
            passed=passed,
            feedback=feedback,
            execution_time=execution_time
        )

        # Actualizar leaderboard si la task fue aceptada
        if passed:
            from .models import Leaderboard
            leaderboard, created = Leaderboard.objects.get_or_create(user=request.user)

            # Verificar si es la primera vez que completa este challenge
            previous_passed = Submission.objects.filter(
                user=request.user,
                challenge=challenge,
                passed=True
            ).exclude(id=submission.id).exists()

            # Si es la primera vez que pasa este challenge, sumar puntos y contar el challenge
            if not previous_passed:
                leaderboard.total_score += challenge.max_score  # Siempre 20 puntos por task
                leaderboard.challenges_completed += 1
                leaderboard.save()

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
    """
    Vista pública del leaderboard - NO requiere autenticación.
    Muestra el ranking de todos los usuarios ordenados por puntuación.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        from .models import Leaderboard

        limit = int(request.query_params.get('limit', 50))

        # Obtener leaderboard ordenado
        leaderboard_entries = Leaderboard.objects.select_related('user').order_by(
            '-total_score', '-challenges_completed', 'last_updated'
        )[:limit]

        leaderboard_data = []
        for idx, entry in enumerate(leaderboard_entries, start=1):
            leaderboard_data.append({
                'rank': idx,
                'username': entry.user.username,
                'total_score': entry.total_score,
                'challenges_completed': entry.challenges_completed,
                'last_updated': entry.last_updated
            })

        # Si el usuario está autenticado, buscar su posición
        user_position = None
        if request.user.is_authenticated:
            try:
                user_entry = Leaderboard.objects.get(user=request.user)
                user_position = user_entry.get_rank()
            except Leaderboard.DoesNotExist:
                user_position = None

        # Si se solicita HTML (navegador), renderizar template
        if 'text/html' in request.headers.get('Accept', ''):
            context = {
                'leaderboard': leaderboard_data,
                'user_position': user_position,
                'total_users': Leaderboard.objects.count()
            }
            return render(request, 'leaderboard.html', context)

        # Si se solicita JSON (API), retornar JSON
        return Response({
            'leaderboard': leaderboard_data,
            'user_position': user_position,
            'total_users': Leaderboard.objects.count()
        })


class ProgressView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from .models import Leaderboard

        user = request.user

        # Obtener o crear entrada de leaderboard
        leaderboard, created = Leaderboard.objects.get_or_create(user=user)

        total_challenges = Challenge.objects.filter(is_active=True).count()
        total_submissions = Submission.objects.filter(user=user).count()
        rank = leaderboard.get_rank()

        return Response({
            'total_score': leaderboard.total_score,
            'challenges_completed': leaderboard.challenges_completed,
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


# ==================== CLIENT DOWNLOAD ====================

class DownloadClientView(views.APIView):
    """
    Vista para descargar el cliente Python directamente desde el servidor
    """
    permission_classes = [AllowAny]

    def get(self, request):
        from django.http import FileResponse, HttpResponse
        import os
        from pathlib import Path
        from django.conf import settings

        # Buscar el archivo del cliente a nivel de manage.py (BASE_DIR)
        # Si BASE_DIR no está definido, calcularlo desde este archivo
        if hasattr(settings, 'BASE_DIR'):
            base_dir = settings.BASE_DIR
        else:
            # views.py está en django_server/grader/views.py
            # manage.py está en django_server/
            base_dir = Path(__file__).resolve().parent.parent

        client_file = base_dir / 'grader_qiskit_client.py'

        if client_file.exists():
            response = FileResponse(
                open(client_file, 'rb'),
                content_type='text/x-python'
            )
            response['Content-Disposition'] = 'attachment; filename="grader_qiskit_client.py"'
            return response
        else:
            # Mostrar información de debug
            import os
            files_in_dir = os.listdir(base_dir) if os.path.exists(base_dir) else []

            return HttpResponse(
                f'<h3>Client file not found</h3>'
                f'<p><strong>Looking for:</strong> {client_file}</p>'
                f'<p><strong>Base directory:</strong> {base_dir}</p>'
                f'<p><strong>Files in directory:</strong></p>'
                f'<ul>{"".join([f"<li>{f}</li>" for f in files_in_dir])}</ul>'
                f'<p>Please make sure "grader_qiskit_client.py" is in the same directory as manage.py</p>',
                status=404
            )


# ==================== HEALTH CHECK ====================

class HealthCheckView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'API is running'
        }, status=status.HTTP_200_OK)
