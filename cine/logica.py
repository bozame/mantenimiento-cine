from datetime import datetime
from .models import Mantenimientos, Equipos

# obtener el próximo estado lógico
def siguiente_estado(actual_estado: int) -> int:
    if actual_estado == 15:
        return 16
    elif actual_estado == 16:
        return 17
    else:
        return actual_estado


# calcular duración del mantenimiento en horas
def duracion_mantenimiento(id_mant: int) -> float:
    try:
        mant = Mantenimientos.objects.get(id_mantenimiento=id_mant)
        if mant.fecha_inicio and mant.fecha_fin:
            diff = mant.fecha_fin - mant.fecha_inicio
            horas = diff.total_seconds() / 3600
            return round(horas, 2)
        return 0.0
    except Mantenimientos.DoesNotExist:
        return 0.0


# 3️⃣ Función: obtener el nombre del equipo asociado a un mantenimiento
def nombre_equipo_mantenimiento(id_mant: int) -> str:
    try:
        mant = Mantenimientos.objects.select_related('id_equipo').get(id_mantenimiento=id_mant)
        return mant.id_equipo.nombre
    except Mantenimientos.DoesNotExist:
        return ""
