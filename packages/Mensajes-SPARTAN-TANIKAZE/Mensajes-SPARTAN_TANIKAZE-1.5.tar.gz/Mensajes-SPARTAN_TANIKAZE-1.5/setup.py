#posee la configuracion para la biblioteca setup toools
from setuptools import setup, find_packages #importar el modulo setup y find_packages para imporautomatizar los packages creando un script que autocomplete esa parte de setuptools

setup( #en la funcion setup hay que indicar una serie de parametros
    name='Mensajes-SPARTAN_TANIKAZE',    #Primero importar el nombre del paquete con el nombre de usuario
    version='1.5',      #Version del paquete, lo modificamos, o lo aumentamos
    description='Un paquete para saludar y despedir',#Descripcion
    long_description=open('README.md').read(), #ingresamos la descripcion larga, que abra el archivo README.md y lea el archivo
    long_description_content_type='text/markdown', #en este campo se aloja el tipo de texto en el que se aloja el archivo de texto para evitar errores en la comprobacion
    author='Miguel Gracia',#Nombre del autor
    author_email='miguelgracia1995@hormail.com', #correo del autor
    url='https://www.youtube.com/channel/UCW6SZMRlvJKmH3JGoTZeJoQ',#Direccion de pagina web
    license_files=['LICENSE'],
    packages=find_packages(),        #Los paquetes que contiene que contiene el ichero __init__
    scripts=[],
    test_suite='tests', #Generamos el test suite y entre comillas la direccion donde se encuentra la carpeta de test
    #scripts=['test.py'], #Los scripts que contiene de manera a raiz
    install_requires=[paquete.strip()
                    for paquete in open ("requirements.txt").readlines()], #si hacemos uso de de comprencion de listas podemos realizar la lectura de los requerimientos que quite los espacios del paquete en la apetura de la lista de requisitos, y lo lea
    #install_requires=['numpy≥1.23.4']  #los paquetes requeridos por el mismo paquete que se va a exportar ≥ que sea mas grande o igual a la instlada
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ] #añadimos los clasificadores que e suna lista que contiene las categorias deonde se puede añadir el tipo de paquete es o su utilidad
    )
#hay que crear en la terminal el siguiente comando:
#           "   python3 setup.py sdist  " 
#para generar el distribuible y nos creara varias carpetas, con el nombre dist


#Cambiamos en la terminal la carpeta dist: "cd dist"

#si hacemos un pip list, podemos ver los paquetes instalados en el pip

#se abre el interprete de python y ejecutamos:
#   from mensajes.hola.saludos import saludar

#Version 1.01
#Para crear una actualizacion, hacemos el cambio, comentamos
#Se realiza el cambio de la version
#y se actualiza con pip install "Nombre de la distribucion.tat.gz" --upgrade


#contruimos el paquete con: python -m build
# comprobamos el paquete con: python -m twine check dist/*
# si todo esta correcto, lo subimos a  pruebas/test a testpypi: con python -m twine upload -r testpypi dist/*
#*nos pedira que nos autotefiquemos

#despues de ver que se encuentra funcionando se sube al repositorio oficial con: python -m twine upload dist/*


#Si se realizara una actualizacion es necesario cambiar el nombre a el directorio dist o borrar para evitar problemas