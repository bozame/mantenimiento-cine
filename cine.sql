-- Ejecutar para crear base de datos en su pc

-- DDL
DROP DATABASE IF EXISTS cine;
create database cine;
use cine;

create table maestra (
  id_maestra int primary key auto_increment,
  nombre varchar(100) not null,
  padre_id int null,
  foreign key (padre_id) references maestra(id_maestra)
);

create table salas (
  id_sala int primary key auto_increment,
  numero int not null,
  capacidad int not null,
  id_estado_func int not null,
  foreign key(id_estado_func) references maestra(id_maestra)
);

create table equipos (
  id_equipo int primary key auto_increment,
  nombre varchar(150) not null,
  id_tipo_eq int not null,
  id_sala int not null,
  id_estado_func int not null,
  foreign key (id_tipo_eq) references maestra(id_maestra),
  foreign key(id_estado_func) references maestra(id_maestra),
  foreign key (id_sala) references salas(id_sala)
);

create table empleados (
  id_empleado int primary key auto_increment,
  nombre varchar(150) not null,
  id_rol int not null,
  id_turno int not null,
  cedula int not null,
  foreign key (id_rol) references maestra(id_maestra),
  foreign key (id_turno) references maestra(id_maestra)
);

create table mantenimientos (
  id_mantenimiento int primary key auto_increment,
  fecha_inicio timestamp not null,
  fecha_fin timestamp null,
  id_tipo_mant int not null,
  id_estado_mant int not null,
  id_equipo int not null,
  id_supervisor int not null,
  descripcion text,
  foreign key(id_estado_mant) references maestra(id_maestra),
  foreign key (id_tipo_mant) references maestra(id_maestra),
  foreign key (id_equipo) references equipos(id_equipo),
  foreign key (id_supervisor) references empleados(id_empleado),
  check (fecha_fin is null or fecha_fin >= fecha_inicio)
);

create table asignaciones (
  id_asignacion int primary key auto_increment,
  id_mantenimiento int not null,
  id_empleado int not null,
  foreign key (id_mantenimiento) references mantenimientos(id_mantenimiento),
  foreign key (id_empleado) references empleados(id_empleado)
);

-- DML

insert into maestra (nombre, padre_id) values
('estado_funcionamiento', null),
('tipo_equipo', null),
('estado_mantenimiento', null),
('tipo_mantenimiento', null),
('turno', null),
('rol', null),
('funcionando', 1),
('requiere mantenimiento', 1),
('en mantenimiento', 1),
('proyector', 2),
('sonido', 2),
('aire acondicionado', 2),
('asientos', 2),
('otros', 2),
('pendiente', 3),
('en progreso', 3),
('completado', 3),
('preventivo', 4),
('correctivo', 4),
('mañana', 5),
('tarde', 5),
('noche', 5),
('técnico', 6),
('supervisor', 6);
select * from maestra;

insert into salas (numero, capacidad, id_estado_func) values
(1, 100, 7),
(2, 80, 7),
(3, 120, 8),
(4, 80, 9),
(5, 150, 7);

insert into equipos (nombre, id_tipo_eq, id_sala, id_estado_func) values
('Proyector Epson X500', 10, 1, 7),
('Sistema de Sonido JBL', 11, 3, 8),
('Aire Samsung 24000 BTU', 12, 2, 7),
('Asientos Reclinables VIP', 13, 4, 9),
('Luces LED Philips', 14, 5, 7);

insert into empleados (nombre, id_rol, id_turno, cedula) values
('Carlos Pérez', 23, 20, 10012345),
('María Gómez', 24, 21, 10067890),
('Luis Rodríguez', 23, 22, 10054321),
('Ana Torres', 24, 20, 10098765),
('Jorge Díaz', 23, 21, 10011223);

INSERT INTO mantenimientos (fecha_inicio, fecha_fin, id_tipo_mant, id_estado_mant, id_equipo, descripcion, id_supervisor) VALUES
('2025-10-01 08:00:00', '2025-10-02 12:00:00', 18, 17, 1, 'Limpieza general del proyector.', 2),
('2025-10-03 09:00:00', NULL, 19, 15, 2, 'Sistema de sonido sin potencia en canal derecho.', 4),
('2025-10-04 08:00:00', '2025-10-04 12:00:00', 18, 17, 3, 'Mantenimiento preventivo del aire acondicionado.', 2),
('2025-10-05 10:30:00', NULL, 19, 16, 4, 'Revisión de asientos dañados en sala 4.', 4),
('2025-10-06 09:00:00', '2025-10-06 16:00:00', 18, 17, 5, 'Cambio de luces LED del techo.', 2);

INSERT INTO asignaciones (id_mantenimiento, id_empleado) VALUES
(1, 1),
(2, 3),
(3, 5),
(4, 1),
(5, 3);

-- 3 VISTAS SQL

-- Muestra cada técnico con los mantenimientos que tiene asignados y sus supervisores.
create view vista_mant_tecnicos as
select 
  asignaciones.id_asignacion,
  empleados.nombre as tecnico,
  empleados2.nombre as supervisor,
  equipos.nombre as equipo,
  maestra.nombre as tipo_mantenimiento,
  maestra2.nombre as estado_mantenimiento
from asignaciones
join empleados on asignaciones.id_empleado = empleados.id_empleado
join mantenimientos on asignaciones.id_mantenimiento = mantenimientos.id_mantenimiento
join empleados as empleados2 on mantenimientos.id_supervisor = empleados2.id_empleado
join equipos on mantenimientos.id_equipo = equipos.id_equipo
join maestra on mantenimientos.id_tipo_mant = maestra.id_maestra
join maestra as maestra2 on mantenimientos.id_estado_mant = maestra2.id_maestra;
select * from vista_mant_tecnicos;

-- lista todos los equipos con su sala y estado de funcionamiento
create view vista_estado_equipos as
select 
    equipos.id_equipo,
    equipos.nombre as equipo,
    salas.numero as sala,
    maestra.nombre as estado
from equipos
join salas on equipos.id_sala = salas.id_sala
join maestra on equipos.id_estado_func = maestra.id_maestra;
select * from vista_estado_equipos;

-- cuenta cuántos mantenimientos ha supervisado cada supervisor
create view vista_supervisores_mantenimientos as
select 
    empleados.nombre as supervisor,
    count(mantenimientos.id_mantenimiento) as total_mantenimientos
from mantenimientos
join empleados on mantenimientos.id_supervisor = empleados.id_empleado
group by empleados.nombre;
select * from vista_supervisores_mantenimientos;


-- FUNCIONES SQL
-- 1. Función para obtener el próximo estado lógico
delimiter //
create function siguiente_estado(actual_estado int)
returns int
deterministic
begin
  declare proximo_estado int;

  if actual_estado = 15 then 
    set proximo_estado = 16;
  elseif actual_estado = 16 then 
    set proximo_estado = 17;
  else 
    set proximo_estado = actual_estado;
  end if;

  return proximo_estado;
end;
//
delimiter ;
-- prueba
update mantenimientos
set id_estado_mant = siguiente_estado(id_estado_mant)
where id_mantenimiento = 2;
select * from mantenimientos where id_mantenimiento = 2;

-- 2. calcular la duración del mantenimiento (en horas)
delimiter //
create function duracion_mantenimiento(id_mant int)
returns decimal(5,2)
deterministic
begin
    declare horas decimal(5,2);
    select 
        timestampdiff(hour, fecha_inicio, fecha_fin)
    into horas
    from mantenimientos
    where id_mantenimiento = id_mant;
    return ifnull(horas, 0);
end;
//
delimiter ;
select duracion_mantenimiento(3);

-- 3. devuelve el nombre del equipo asociado a un mantenimiento
delimiter //
create function nombre_equipo_mantenimiento(id_mant int)
returns varchar(150)
deterministic
begin
    declare equipo_nom varchar(150);
    select equipos.nombre into equipo_nom
    from mantenimientos
    join equipos on mantenimientos.id_equipo = equipos.id_equipo
    where mantenimientos.id_mantenimiento = id_mant;
    return equipo_nom;
end;
//
delimiter ;
select nombre_equipo_mantenimiento(4);



-- 	TRIGGERS SQL
-- actualizar automáticamente el estado del mantenimiento
delimiter //
create trigger actualizar_estado_mantenimiento
before update on mantenimientos
for each row
begin
  if old.fecha_fin is null and new.fecha_fin is not null then
    set new.id_estado_mant = siguiente_estado(old.id_estado_mant);
  end if;
end;
//
delimiter ;
-- prueba
select * from mantenimientos;
update mantenimientos
set fecha_fin = '2025-10-03 18:00:00'
where id_mantenimiento = 2;

-- evita que un técnico se asigne dos veces en un mismo mantenimiento
delimiter //
create trigger prevenir_asignacion_duplicada
before insert on asignaciones
for each row
begin
  if exists (
    select * from asignaciones 
    where id_mantenimiento = new.id_mantenimiento 
      and id_empleado = new.id_empleado
  ) then
    signal sqlstate '45000'
    set message_text = 'este técnico ya está asignado a este mantenimiento.';
  end if;
end
//
delimiter ;
-- prueba
-- insert into asignaciones (id_mantenimiento, id_empleado)
-- values (1, 1);

-- evita que un supervisor (rol id=24) sea asignado como técnico en la tabla asignaciones
delimiter //
create trigger evitar_supervisor_tecnico
before insert on asignaciones
for each row
begin
    declare rol int;
    select id_rol into rol
    from empleados
    where id_empleado = new.id_empleado;
    if rol = 24 then
        signal sqlstate '45000'
        set message_text = 'no se puede asignar un supervisor como técnico en un mantenimiento.';
    end if;
end;
//
delimiter ;
-- prueba
-- insert into asignaciones (id_mantenimiento, id_empleado)
-- values (1, 2);