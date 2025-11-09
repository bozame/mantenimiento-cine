# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Maestra(models.Model):
    id_maestra = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    padre = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maestra'


    def __str__(self):
        return self.nombre or f"Maestra {self.id_maestra}"

class Salas(models.Model):
    id_sala = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    capacidad = models.IntegerField()
    id_estado_func = models.ForeignKey(Maestra, models.DO_NOTHING, db_column='id_estado_func')

    class Meta:
        managed = False
        db_table = 'salas'

    def __str__(self):
        return f"Sala {self.numero} ({self.capacidad} personas)"

class Equipos(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    id_tipo_eq = models.ForeignKey('Maestra', models.DO_NOTHING, db_column='id_tipo_eq')
    id_sala = models.ForeignKey('Salas', models.DO_NOTHING, db_column='id_sala')
    id_estado_func = models.ForeignKey('Maestra', models.DO_NOTHING, db_column='id_estado_func', related_name='equipos_id_estado_func_set')

    class Meta:
        managed = False
        db_table = 'equipos'

    def __str__(self):
        return f"{self.nombre} - {self.id_sala}"

class Empleados(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    id_rol = models.ForeignKey('Maestra', models.DO_NOTHING, db_column='id_rol')
    id_turno = models.ForeignKey('Maestra', models.DO_NOTHING, db_column='id_turno', related_name='empleados_id_turno_set')
    cedula = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'empleados'

    def __str__(self):
        return f"{self.nombre} ({self.id_rol})"

class Mantenimientos(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(blank=True, null=True)
    id_tipo_mant = models.ForeignKey(Maestra, models.DO_NOTHING, db_column='id_tipo_mant')
    id_estado_mant = models.ForeignKey(Maestra, models.DO_NOTHING, db_column='id_estado_mant', related_name='mantenimientos_id_estado_mant_set')
    id_equipo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo')
    id_supervisor = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_supervisor')
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos'

    def __str__(self):
        return f"{self.id_tipo_mant} - {self.id_equipo} ({self.id_estado_mant})"

class Asignaciones(models.Model):
    id_asignacion = models.AutoField(primary_key=True)
    id_mantenimiento = models.ForeignKey('Mantenimientos', models.DO_NOTHING, db_column='id_mantenimiento')
    id_empleado = models.ForeignKey('Empleados', models.DO_NOTHING, db_column='id_empleado')

    class Meta:
        managed = False
        db_table = 'asignaciones'

    def __str__(self):
        return f"{self.id_empleado} asignado a {self.id_mantenimiento}"