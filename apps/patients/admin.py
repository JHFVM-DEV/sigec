from django.contrib import admin
from .models import (
    Patient, ClinicalProfile, VitalSigns, Allergy, 
    PatientAllergy, EmergencyContact, BloodType, InsuranceProvider
)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['ci', 'phone', 'date_of_birth', 'gender', 'created_at']
    search_fields = ['ci', 'phone', 'address']
    list_filter = ['gender', 'created_at']


@admin.register(ClinicalProfile)
class ClinicalProfileAdmin(admin.ModelAdmin):
    list_display = ['patient', 'blood_type']
    search_fields = ['patient__ci']


@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'blood_pressure', 'temperature', 'measured_by']
    list_filter = ['date']


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity']


admin.site.register([PatientAllergy, EmergencyContact, BloodType, InsuranceProvider])