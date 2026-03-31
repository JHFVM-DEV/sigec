"""
URL configuration for sigec project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from apps.core.api.router import core_router

api = NinjaAPI(
    title = "SIGEC API",
    version = "1.0",
    description = "API para el Sistema de Gestión Clínica con Módulo de Administración y Triage Inteligente (SIGEC)",
    docs_url = "/docs"
)

api.add_router("", core_router)  # Agrega las rutas de NinjaAPI al enrutador principal

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),  # Agrega las rutas de NinjaAPI bajo el prefijo 'api/'
]
