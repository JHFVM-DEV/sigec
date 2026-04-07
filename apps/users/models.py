from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El correo electrónico es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('El superusuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('El superusuario debe tener is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
    
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del rol")
    description = models.TextField(blank=True, verbose_name="Descripción del rol")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="Nombre")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Apellido")
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")
    is_staff = models.BooleanField(default=False, verbose_name="¿Es personal?")
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Rol", null=True, blank=True, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    is_doctor=models.BooleanField(default=False, verbose_name="¿Es doctor?")
    is_nurse=models.BooleanField(default=False, verbose_name="¿Es enfermera/o?")
    speciality=models.CharField(max_length=100, blank=True, verbose_name="Especialidad médica")

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    phone = models.CharField(max_length=20, blank=True, verbose_name="Número de teléfono")
    identification_number = models.CharField(max_length=20, blank=True, verbose_name="Número de CI/NIT")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'identification_number']

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.email}"
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]