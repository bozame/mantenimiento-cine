# Después de clonar:

## Base de datos
El programa funciona con una base de datos local, así que primero debe crear la base de datos en su máquina. Hay un archivo cine.sql que puede ejecutar en Workbench para crear la BD en su pc, y luego ajustar la conexión desde mantenimiento_cine > setting.py de ser necesario justo en la parte que dice algo como esto:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cine',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

## Instalar lo necesario

Ejecutar "pip install Django" en consola de no tenerlo instalado.