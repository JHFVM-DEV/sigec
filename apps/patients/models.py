from django.db import models
from django.utils import timezone
from apps.core.models import AuditableModel
from apps.users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


class BloodType(models.Model):
    group = models.CharField(max_length=2, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')])
    rh = models.CharField(max_length=1, choices=[('+', '+'), ('-', '-')])
    
    class Meta:
        verbose_name = "Tipo de Sangre"
        verbose_name_plural = "Tipos de Sangre"
        unique_together = ('group', 'rh')

    def __str__(self):
        return f"{self.group}{self.rh}"


class InsuranceProvider(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre de la Aseguradora")
    code = models.CharField(max_length=50, unique=True, verbose_name="Código")
    patient_type = models.CharField(max_length=100, blank=True, verbose_name="Tipo de Paciente")
    policy_number = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Proveedor de Seguro"
        verbose_name_plural = "Proveedores de Seguro"

    def __str__(self):
        return self.name


class Patient(AuditableModel):
    """Modelo principal de Paciente"""
    ci = models.CharField(max_length=20, unique=True, verbose_name="Cédula de Identidad")
    ci_complement = models.CharField(max_length=10, blank=True, verbose_name="Complemento CI")
    date_of_birth = models.DateField(verbose_name="Fecha de Nacimiento")
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    marital_status = models.CharField(max_length=50, blank=True, verbose_name="Estado Civil")
    occupation = models.CharField(max_length=150, blank=True, verbose_name="Ocupación")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True, verbose_name="Dirección")
    
    insurance_provider = models.ForeignKey(
        InsuranceProvider, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Aseguradora Principal"
    )
    photo_url = models.URLField(blank=True, verbose_name="URL de Foto")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ci} - {self.get_full_name()}"

    def get_full_name(self):
        # Podremos agregar first_name y last_name más adelante si lo necesitamos vía perfil
        return f"Paciente {self.ci}"


class ClinicalProfile(AuditableModel):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='clinical_profile')
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL, null=True, blank=True)
    chronic_diseases = models.TextField(blank=True, verbose_name="Enfermedades Crónicas")
    family_history = models.TextField(blank=True, verbose_name="Antecedentes Familiares")
    habit = models.TextField(blank=True, verbose_name="Hábitos")
    surgical_history = models.TextField(blank=True, verbose_name="Antecedentes Quirúrgicos")
    transfusion_history = models.TextField(blank=True, verbose_name="Antecedentes de Transfusiones")

    class Meta:
        verbose_name = "Perfil Clínico"
        verbose_name_plural = "Perfiles Clínicos"

    def __str__(self):
        return f"Perfil clínico de {self.patient}"


class VitalSigns(AuditableModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Altura (cm)")
    blood_pressure = models.CharField(max_length=20, blank=True, verbose_name="Presión Arterial (ej: 120/80)")
    heart_rate = models.IntegerField(null=True, blank=True, verbose_name="Frecuencia Cardíaca")
    respiratory_rate = models.IntegerField(null=True, blank=True, verbose_name="Frecuencia Respiratoria")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura (°C)")
    oxygen_saturation = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    date = models.DateTimeField(default=timezone.now)
    measured_by = models.ForeignKey(
        'users.CustomUser', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='measured_vitals'
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Signo Vital"
        verbose_name_plural = "Signos Vitales"
        ordering = ['-date']

    def __str__(self):
        return f"Signos vitales de {self.patient} - {self.date}"


class Allergy(AuditableModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=50, choices=[
        ('MILD', 'Leve'), ('MODERATE', 'Moderada'), ('SEVERE', 'Severa'), ('CRITICAL', 'Crítica')
    ])

    class Meta:
        verbose_name = "Alergia"
        verbose_name_plural = "Alergias"

    def __str__(self):
        return self.name


class PatientAllergy(AuditableModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies')
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)
    severity = models.CharField(max_length=50, choices=Allergy._meta.get_field('severity').choices)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Alergia del Paciente"
        verbose_name_plural = "Alergias del Paciente"
        unique_together = ('patient', 'allergy')

    def __str__(self):
        return f"{self.allergy} - {self.patient}"


class EmergencyContact(AuditableModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100, verbose_name="Relación")
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Contacto de Emergencia"
        verbose_name_plural = "Contactos de Emergencia"

    def __str__(self):
        return f"{self.name} ({self.relationship})"