from django.db import models
from django.contrib.contenttypes.models import ContentType
from apps.audit.models import AuditLog
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json
from django.utils import timezone

class AuditableModel(models.Model):
    """
    Mixin abstracto que permite que cualquier modelo herede auditoría automática.
    Todos los modelos clínicos importantes deben heredar de esta clase.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        abstract = True  # ← Muy importante: no crea tabla

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Guardamos el estado original para detectar cambios
        self._original_state = {field.attname: getattr(self, field.attname) for field in self._meta.fields}

    def get_changed_fields(self):
        """Retorna solo los campos que realmente cambiaron"""
        if not hasattr(self, '_original_state'):
            return {}
        
        changed = {}
        for field in self._meta.fields:
            field_name = field.attname
            old_value = self._original_state.get(field_name)
            new_value = getattr(self, field_name)
            if old_value != new_value:
                changed[field_name] = {
                    'old': old_value,
                    'new': new_value
                }
        return changed


# ==================== SEÑALES GLOBALES DE AUDITORÍA ====================

@receiver(post_save)
def audit_post_save(sender, instance, created, **kwargs):
    """Registra creación y actualización"""
    # Ignoramos tablas internas de Django y la propia tabla de auditoría
    if sender._meta.app_label in ['admin', 'contenttypes', 'sessions', 'audit']:
        return

    if not isinstance(instance, AuditableModel):
        return

    action = 'CREATE' if created else 'UPDATE'
    changed_fields = instance.get_changed_fields() if not created else {}

    user = kwargs.get('user', None)   # Se podrá pasar desde middleware más adelante

    if created:
        # Para creación, registramos el evento general
        AuditLog.objects.create(
            user=user,
            action=action,
            affected_table=sender._meta.db_table,
            register_id=instance.pk,
            module=sender._meta.app_label,
            notes=f"Registro creado"
        )
    else:
        # Para actualización, registramos cada campo cambiado
        for field_name, values in changed_fields.items():
            AuditLog.objects.create(
                user=user,
                action=action,
                affected_table=sender._meta.db_table,
                affected_column=field_name,
                old_value=str(values['old'])[:500] if values['old'] is not None else None,
                new_value=str(values['new'])[:500],
                register_id=instance.pk,
                module=sender._meta.app_label,
            )


@receiver(post_delete)
def audit_post_delete(sender, instance, **kwargs):
    """Registra eliminaciones"""
    if sender._meta.app_label in ['admin', 'contenttypes', 'sessions', 'audit']:
        return

    if not isinstance(instance, AuditableModel):
        return

    AuditLog.objects.create(
        user=kwargs.get('user', None),
        action='DELETE',
        affected_table=sender._meta.db_table,
        register_id=instance.pk,
        module=sender._meta.app_label,
        notes=f"Registro eliminado"
    )