# backend/apps/core/api/router.py
from ninja import Router

# Creamos el router con un nombre claro
core_router = Router(tags=["Core"], auth=None)

@core_router.get("/health-check", response=dict)
def health_check(request):
    """Endpoint de verificación del estado del backend"""
    return {
        "status": "success",
        "message": "SIGEC Backend funcionando correctamente 🚀",
        "version": "1.0.0",
        "environment": "development"
    }

@core_router.get("/ping")
def ping(request):
    """Endpoint simple para pruebas rápidas"""
    return {"message": "pong"}