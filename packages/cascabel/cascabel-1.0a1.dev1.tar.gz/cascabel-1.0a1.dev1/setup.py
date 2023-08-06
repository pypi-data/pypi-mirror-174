from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


import os

archivos = []

dir_file = str(os.getcwd() + '/cascabel')
for nombre_directorio, dirs, ficheros in os.walk(dir_file):
    if nombre_directorio.find('__pycache__') == -1:
        directorio = nombre_directorio.replace(dir_file + '\\', '').replace(dir_file, '').replace('\\', '/')
        if directorio != 'cascabel' and directorio != '':
            for nombre_fichero in ficheros:
                archivos.append(directorio + '/' + nombre_fichero)

VERSION = '1.0a1.dev1'

file = open('cascabel/classes/cascabel.py', 'r')

import re

contenido = re.sub( 'VERSION = ".*"', f'VERSION = "{VERSION}"' ,file.read())

file.close()

file = open('cascabel/classes/cascabel.py', 'w')
file.write(contenido)
file.close()

DESCRIPTION = 'Agiliza la creción de páginas web con Flask'
LONG_DESCRIPTION = 'Un paquete que te permitira agilizar la creación de paginas web mediante flask.'

# Setting up
setup(
    name="cascabel",
    version=VERSION,
    author="Ignacio Aguilera Oyaneder",
    author_email="<ignacio.a.o@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['colorama', 'flask', 'python-dotenv'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data = {
        '': archivos
    },
    include_package_data=True,
    entry_points={'console_scripts':['cascabel = cascabel:main'] }
)