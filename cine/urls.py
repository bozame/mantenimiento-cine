from django.urls import path
from . import views

urlpatterns = [
    path('vista-mant-tecnicos/', views.vista_mant_tecnicos, name='vista_mant_tecnicos'),
    path('vista-estado-equipos/', views.vista_estado_equipos, name='vista_estado_equipos'),
    path('vista-supervisores/', views.vista_supervisores_mantenimientos, name='vista_supervisores_mantenimientos'),

    path('salas/', views.salas, name='salas'),
    path('salas/guardar/', views.guardar_sala, name='guardar_sala'),
    path('salas/eliminar/<int:id_sala>/', views.eliminar_sala, name='eliminar_sala'),

    path('equipos/', views.equipos, name='equipos'),
    path('equipos/guardar/', views.guardar_equipo, name='guardar_equipo'),
    path('equipos/eliminar/<int:id_equipo>/', views.eliminar_equipo, name='eliminar_equipo'),

    path('empleados/', views.empleados, name='empleados'),
    path('empleados/guardar/', views.guardar_empleado, name='guardar_empleado'),
    path('empleados/eliminar/<int:id_empleado>/', views.eliminar_empleado, name='eliminar_empleado'),

    path('mantenimientos/', views.mantenimientos, name='mantenimientos'),
    path('mantenimientos/guardar/', views.guardar_mantenimiento, name='guardar_mantenimiento'),
    path('mantenimientos/eliminar/<int:id_mantenimiento>/', views.eliminar_mantenimiento, name='eliminar_mantenimiento'),

    path('asignaciones/', views.asignaciones, name='asignaciones'),
    path('asignaciones/guardar/', views.guardar_asignacion, name='guardar_asignacion'),
    path('asignaciones/eliminar/<int:id_asignacion>/', views.eliminar_asignacion, name='eliminar_asignacion'),

    path('vistas/', views.vistas, name='vistas'),
    path('crear_mantenimiento_con_asignacion/', views.crear_mantenimiento_con_asignacion, name='crear_mantenimiento_con_asignacion'),
]
