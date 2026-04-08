from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Rol")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'role'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    role = models.ForeignKey(
        Role, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='users',
        verbose_name="Rol del Usuario"
    )

    class Meta:
        db_table = 'auth_user' # Mantenemos el nombre que pediste en tu diseño

    def __str__(self):
        return f"{self.username} - {self.role.name if self.role else 'Sin rol'}"