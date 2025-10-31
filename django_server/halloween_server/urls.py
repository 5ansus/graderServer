"""
URL configuration for halloween_server project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def root_view(request):
    """Vista raíz que redirige a la API"""
    return JsonResponse({
        'message': '🎃 Halloween Qiskit Challenge API',
        'api': '/api/',
        'admin': '/admin/',
        'health': '/api/health',
        'documentation': 'https://github.com/5ansus/graderServer',
    })

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('grader.urls')),
]
