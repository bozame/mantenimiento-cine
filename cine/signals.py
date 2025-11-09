from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Mantenimientos, Asignaciones, Empleados
from .logica import siguiente_estado


# actualizar automáticamente el estado del mantenimiento
@receiver(pre_save, sender=Mantenimientos)
def actualizar_estado_mantenimiento(sender, instance, **kwargs):
    if not instance.pk:
        return 

    anterior = Mantenimientos.objects.filter(pk=instance.pk).first()
    if not anterior:
        return

    if anterior.fecha_fin is None and instance.fecha_fin is not None:
        instance.id_estado_mant_id = siguiente_estado(anterior.id_estado_mant_id)


# evitar que un técnico se asigne dos veces al mismo mantenimiento
@receiver(pre_save, sender=Asignaciones)
def prevenir_asignacion_duplicada(instance):
    if Asignaciones.objects.filter(
        id_mantenimiento=instance.id_mantenimiento,
        id_empleado=instance.id_empleado
    ).exclude(pk=instance.pk).exists():
        raise ValidationError("ERROR, Este técnico ya está asignado a este mantenimiento.")


# evitar que un supervisor sea asignado como técnico
@receiver(pre_save, sender=Asignaciones)
def evitar_supervisor_tecnico( instance):
    empleado = instance.id_empleado
    if empleado and empleado.id_rol_id == 24:
        raise ValidationError("ERROR, No se puede asignar un supervisor como técnico en un mantenimiento.")
