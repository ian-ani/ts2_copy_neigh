[![Lang en](https://img.shields.io/badge/lang-en-blue?style=flat)](https://github.com/ian-ani/ts2_copy_neigh/blob/main/README.md)
[![Lang es](https://img.shields.io/badge/lang-es-red?style=flat)](https://github.com/ian-ani/ts2_copy_neigh/blob/main/README.es.md)

## Tabla de contenidos

- [Acerca de este repositorio](#Acerca-de-este-repositorio)
- [Hecho con](#Hecho-con)
- [Uso](#Uso)
- [Por hacer](#Por-hacer)

## Acerca de este repositorio

Programa creado con **Python** para la copia de un barrio de **Los Sims 2** a elección del usuario.
Si el barrio ya existe incrementará el número de la ID del barrio y también lo hará con los archivos
correspondientes dentro de los subdirectorios.  
Probado con Windows 10 y **Los Sims 2 - Ultimate Collection**.

## Hecho con

- os
- tkinter
- shutil
- pathlib
- json
- webbrowser

## Uso

1. Hacer clic en **Ruta de origen** para elegir la ruta de origen del barrio. 
Para más información, clic en **Ayuda**.
2. Hacer clic en **Ruta de destino** para elegir la ruta de destino donde se guardará el barrio.
Para más información, clic en **Ayuda**.
3. Hacer clic en **Ejecutar** para hacer la copia.
4. El botón de **Ayuda** proporciona más información sobre el uso del programa.
5. El botón **Idioma** permite elegir entre inglés y español.

## Por hacer

- Manejo de errores y excepciones.
- Refactorización de código (hay redundancia).
- Ordenar los archivos en directorios con nombres más apropiados.
- Mejorar la salida por pantalla de los pasos que están sucediendo.