"""
URL configuration for halloween_server project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('grader.urls')),  # Incluye las URLs de grader (con home en raíz)
    path('admin/', admin.site.urls),
]
