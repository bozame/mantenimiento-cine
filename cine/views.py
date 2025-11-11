from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, F
from .models import Asignaciones, Equipos, Empleados, Mantenimientos, Salas, Maestra
from .forms import SalaForm
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .logica import duracion_mantenimiento

def index(request):
    empleados = Empleados.objects.all()
    salas = Salas.objects.all()
    equipos = Equipos.objects.all()
    mantenimientos = Mantenimientos.objects.all()
    asignaciones = Asignaciones.objects.all()
    maestra = Maestra.objects.all()
    return render(request, 'index.html', {
        'empleados': empleados,
        'salas': salas,
        'equipos': equipos,
        'mantenimientos': mantenimientos,
        'asignaciones': asignaciones,
        'maestra': maestra
    })


def vista_mant_tecnicos(request):
    datos = (
        Asignaciones.objects
        .select_related('id_empleado', 'id_mantenimiento__id_equipo', 'id_mantenimiento__id_supervisor')
        .select_related('id_mantenimiento__id_tipo_mant', 'id_mantenimiento__id_estado_mant')
        .values(
            'id_asignacion',
            tecnico=models.F('id_empleado__nombre'),
            supervisor=models.F('id_mantenimiento__id_supervisor__nombre'),
            equipo=models.F('id_mantenimiento__id_equipo__nombre'),
            tipo_mantenimiento=models.F('id_mantenimiento__id_tipo_mant__nombre'),
            estado_mantenimiento=models.F('id_mantenimiento__id_estado_mant__nombre'),
        )
    )
    return render(request, 'vista_mant_tecnicos.html', {'datos': datos})

def vista_estado_equipos(request):
    datos = (
        Equipos.objects
        .select_related('id_sala', 'id_estado_func')
        .values(
            'id_equipo',
            equipo=models.F('nombre'),
            sala=models.F('id_sala__numero'),
            estado=models.F('id_estado_func__nombre'),
        )
    )
    return render(request, 'vista_estado_equipos.html', {'datos': datos})

def vista_supervisores_mantenimientos(request):
    datos = (
        Empleados.objects
        .filter(mantenimientos__id_supervisor=models.F('id_empleado'))
        .annotate(total_mantenimientos=Count('mantenimientos'))
        .values('nombre', 'total_mantenimientos')
    )
    return render(request, 'vista_supervisores_mantenimientos.html', {'datos': datos})


# ----------------- CRUD SALAS--------------------
def salas(request):
    salas = Salas.objects.all()
    maestra = Maestra.objects.filter(padre=1)
    return render(request, 'salas.html', {
        'salas': salas,
        'maestra': maestra
        })

# crear o editar
def guardar_sala(request):
    if request.method == 'POST':
        id_sala = request.POST.get('id_sala')
        numero = request.POST.get('numero')
        capacidad = request.POST.get('capacidad')
        id_estado_func = request.POST.get('id_estado_func')

        estado = get_object_or_404(Maestra, id_maestra=id_estado_func)

        if id_sala not in (None, ""):
            sala = get_object_or_404(Salas, id_sala=id_sala)
            sala.numero = numero
            sala.capacidad = capacidad
            sala.id_estado_func = estado
            sala.save()
        else:
            Salas.objects.create(numero=numero, capacidad=capacidad, id_estado_func=estado)

    return redirect('salas')

# Eliminar Sala

def eliminar_sala(request, id_sala):
    sala = get_object_or_404(Salas, id_sala=id_sala)
    sala.delete()
    return redirect('salas')

# ----------------- CRUD EQUIPOS --------------------
def equipos(request):
    equipos = Equipos.objects.all()
    salas = Salas.objects.all()
    tipos_eq = Maestra.objects.filter(padre=2)
    estado_func = Maestra.objects.filter(padre=1)
    return render(request, 'equipos.html', {
        'equipos': equipos,
        'salas': salas,
        'tipos_eq': tipos_eq,
        'estado_func': estado_func,
    })

def guardar_equipo(request):
    if request.method == 'POST':
        id_equipo = request.POST.get('id_equipo')
        nombre = request.POST.get('nombre')
        id_tipo_eq = request.POST.get('id_tipo_eq')
        id_sala = request.POST.get('id_sala')
        id_estado_func = request.POST.get('id_estado_func')

        tipo = get_object_or_404(Maestra, id_maestra=id_tipo_eq)
        estado = get_object_or_404(Maestra, id_maestra=id_estado_func)
        sala = get_object_or_404(Salas, id_sala=id_sala)

        if id_equipo:
            equipo = get_object_or_404(Equipos, id_equipo=id_equipo)
            equipo.nombre = nombre
            equipo.id_tipo_eq = tipo
            equipo.id_sala = sala
            equipo.id_estado_func = estado
            equipo.save()
        else:  # Crear
            Equipos.objects.create(
                nombre=nombre,
                id_tipo_eq=tipo,
                id_sala=sala,
                id_estado_func=estado
            )

    return redirect('equipos')

def eliminar_equipo(request, id_equipo):
    equipo = get_object_or_404(Equipos, id_equipo=id_equipo)
    equipo.delete()
    return redirect('equipos')


# ------------------- CRUD EMPLEADOS ----------------------
def empleados(request):
    empleados = Empleados.objects.all()
    rol = Maestra.objects.filter(padre=6)
    turno = Maestra.objects.filter(padre=5)
    return render(request, 'empleados.html', {
        'empleados': empleados,
        'rol':rol,
        'turno':turno,
        })

def guardar_empleado(request):
    if request.method == 'POST':
        id_empleado = request.POST.get('id_empleado')
        nombre = request.POST.get('nombre')
        id_rol = request.POST.get('id_rol')
        id_turno = request.POST.get('id_turno')
        cedula = request.POST.get('cedula')

        rol = get_object_or_404(Maestra, id_maestra=id_rol)
        turno = get_object_or_404(Maestra, id_maestra=id_turno)

        if id_empleado:
            emp = get_object_or_404(Empleados, id_empleado=id_empleado)
            emp.nombre = nombre
            emp.id_rol = rol
            emp.id_turno = turno
            emp.cedula = cedula
            emp.save()
        else:
            Empleados.objects.create(nombre=nombre, id_rol=rol, id_turno=turno, cedula=cedula)

    return redirect('empleados')

def eliminar_empleado(request, id_empleado):
    emp = get_object_or_404(Empleados, id_empleado=id_empleado)
    emp.delete()
    return redirect('empleados')

# ---------------- CRUD MANTENIMIENTOS ---------------

def mantenimientos(request):
    mantenimientos_obj = Mantenimientos.objects.select_related(
        'id_tipo_mant', 'id_estado_mant', 'id_equipo', 'id_supervisor'
    ).order_by('id_mantenimiento') 

    mantenimientos = []
    for m in mantenimientos_obj:
        mantenimientos.append({
            'id_mantenimiento': m.id_mantenimiento,
            'fecha_inicio': m.fecha_inicio,
            'fecha_fin': m.fecha_fin,
            'id_tipo_mant': m.id_tipo_mant,
            'id_estado_mant': m.id_estado_mant,
            'id_equipo': m.id_equipo,
            'id_supervisor': m.id_supervisor,
            'descripcion': m.descripcion,
            'duracion': duracion_mantenimiento(m.id_mantenimiento)  # <-- calculamos la duración
        })

    estado_mant = Maestra.objects.filter(padre=3)
    tipo_mant = Maestra.objects.filter(padre=4)
    equipos = Equipos.objects.all() 
    empleados = Empleados.objects.filter(id_rol=24)
    return render(request, 'mantenimientos.html', {
        'mantenimientos': mantenimientos,
        'estado_mant': estado_mant,
        'tipo_mant': tipo_mant,
        'equipos': equipos,
        'empleados': empleados
    })

def guardar_mantenimiento(request):
    if request.method == 'POST':
        id_mantenimiento = request.POST.get('id_mantenimiento')
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')
        id_tipo_mant = request.POST.get('id_tipo_mant')
        id_estado_mant = request.POST.get('id_estado_mant')
        id_equipo = request.POST.get('id_equipo')
        id_supervisor = request.POST.get('id_supervisor')
        descripcion = request.POST.get('descripcion')

        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%dT%H:%M'))
        fecha_fin = None
        if fecha_fin_str:
            fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%dT%H:%M'))

        tipo_mant = get_object_or_404(Maestra, id_maestra=id_tipo_mant)
        estado_mant = get_object_or_404(Maestra, id_maestra=id_estado_mant)
        equipo = get_object_or_404(Equipos, id_equipo=id_equipo)
        supervisor = get_object_or_404(Empleados, id_empleado=id_supervisor)

        if id_mantenimiento: 
            mantenimiento = get_object_or_404(Mantenimientos, id_mantenimiento=id_mantenimiento)
            mantenimiento.id_tipo_mant = tipo_mant
            mantenimiento.id_estado_mant = estado_mant
            mantenimiento.id_equipo = equipo
            mantenimiento.id_supervisor = supervisor
            mantenimiento.fecha_inicio = fecha_inicio
            mantenimiento.fecha_fin = fecha_fin
            mantenimiento.descripcion = descripcion
            mantenimiento.save()
        else:
            Mantenimientos.objects.create(
                id_tipo_mant=tipo_mant,
                id_estado_mant=estado_mant,
                id_equipo=equipo,
                id_supervisor=supervisor,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                descripcion=descripcion
            )

    return redirect('mantenimientos')

def eliminar_mantenimiento(request, id_mantenimiento):
    mant = get_object_or_404(Mantenimientos, id_mantenimiento=id_mantenimiento)
    mant.delete()
    return redirect('mantenimientos')


# -------------- CRUD ASIGNACIONES --------------------
def asignaciones(request):
    asignaciones = Asignaciones.objects.all()
    mantenimientos = Mantenimientos.objects.all()
    empleados = Empleados.objects.all()
    return render(request, 'asignaciones.html', {
        'asignaciones': asignaciones,
        'mantenimientos': mantenimientos,
        'empleados': empleados
    })

def guardar_asignacion(request):
    if request.method == 'POST':
        id_asignacion = request.POST.get('id_asignacion')
        mantenimiento_id = request.POST.get('id_mantenimiento')
        empleado_id = request.POST.get('id_empleado')

        mantenimiento = get_object_or_404(Mantenimientos, id_mantenimiento=mantenimiento_id)
        empleado = get_object_or_404(Empleados, id_empleado=empleado_id)

        if id_asignacion:
            asignacion = get_object_or_404(Asignaciones, id_asignacion=id_asignacion)
            asignacion.id_mantenimiento = mantenimiento
            asignacion.id_empleado = empleado
            asignacion.save()
        else:
            Asignaciones.objects.create(
                id_mantenimiento=mantenimiento,
                id_empleado=empleado
            )

    return redirect('asignaciones')

def eliminar_asignacion(request, id_asignacion):
    asignacion = get_object_or_404(Asignaciones, id_asignacion=id_asignacion)
    asignacion.delete()
    return redirect('asignaciones')

# ------------- VISTAS ---------------------
def vistas(request):
    # Muestra cada técnico con los mantenimientos que tiene asignados y sus supervisores.
    mant_tecnicos = (
        Asignaciones.objects
        .select_related('id_empleado', 'id_mantenimiento__id_equipo', 'id_mantenimiento__id_supervisor')
        .select_related('id_mantenimiento__id_tipo_mant', 'id_mantenimiento__id_estado_mant')
        .values(
            'id_asignacion',
            tecnico=F('id_empleado__nombre'),
            supervisor=F('id_mantenimiento__id_supervisor__nombre'),
            equipo=F('id_mantenimiento__id_equipo__nombre'),
            tipo_mantenimiento=F('id_mantenimiento__id_tipo_mant__nombre'),
            estado_mantenimiento=F('id_mantenimiento__id_estado_mant__nombre'),
        )
    )

    # lista todos los equipos con su sala y estado de funcionamiento
    estado_equipos = (
        Equipos.objects
        .select_related('id_sala', 'id_estado_func')
        .values(
            'id_equipo',
            equipo=F('nombre'),
            sala=F('id_sala__numero'),
            estado=F('id_estado_func__nombre'),
        )
    )

    # cuenta cuántos mantenimientos ha supervisado cada supervisor
    supervisores = (
        Empleados.objects
        .filter(mantenimientos__id_supervisor=F('id_empleado'))
        .annotate(total_mantenimientos=Count('mantenimientos'))
        .values('nombre', 'total_mantenimientos')
    )

    context = {
        'mant_tecnicos': mant_tecnicos,
        'estado_equipos': estado_equipos,
        'supervisores': supervisores,
    }

    return render(request, 'vistas.html', context)


from django.contrib import messages

def crear_mantenimiento_con_asignacion(request):
    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')
        id_tipo_mant = request.POST.get('id_tipo_mant')
        id_estado_mant = request.POST.get('id_estado_mant')
        id_equipo = request.POST.get('id_equipo')
        id_supervisor = request.POST.get('id_supervisor')
        descripcion = request.POST.get('descripcion')
        id_empleado = request.POST.get('id_empleado')

        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%dT%H:%M'))
        fecha_fin = None
        if fecha_fin_str:
            fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%dT%H:%M'))

        tipo_mant = get_object_or_404(Maestra, id_maestra=id_tipo_mant)
        estado_mant = get_object_or_404(Maestra, id_maestra=id_estado_mant)
        equipo = get_object_or_404(Equipos, id_equipo=id_equipo)
        supervisor = get_object_or_404(Empleados, id_empleado=id_supervisor)
        empleado = get_object_or_404(Empleados, id_empleado=id_empleado)

        # guardar mantenimiento
        mantenimiento = Mantenimientos.objects.create(
            id_tipo_mant=tipo_mant,
            id_estado_mant=estado_mant,
            id_equipo=equipo,
            id_supervisor=supervisor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            descripcion=descripcion
        )

        # guardar asignación
        Asignaciones.objects.create(
            id_mantenimiento=mantenimiento,
            id_empleado=empleado
        )
        
        messages.success(request, '✅ Mantenimiento y asignación creados correctamente.')

        return redirect('crear_mantenimiento_con_asignacion')  # redirige al mismo formulario

    #get
    equipos = Equipos.objects.all()
    empleados = Empleados.objects.all()
    tipos = Maestra.objects.filter(padre__nombre='tipo_mantenimiento')
    estados = Maestra.objects.filter(padre__nombre='estado_mantenimiento')

    return render(request, 'crear_mantenimiento.html', {
        'equipos': equipos,
        'empleados': empleados,
        'tipos': tipos,
        'estados': estados
    })
