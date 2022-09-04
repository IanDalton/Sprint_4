<!--
Nombre del proyecto
Descripción del proyecto
Dependencias. Esto es, lo que necesito para poder ejecutar el programa (Python 3.9, etc.) y las librerías externas (si lo requiere). En el caso de que el programa necesite librerías externas indicar cómo se instalan.
Cómo ejecuto el programa: debe constar el comando para poder ejecutar el programa así como también un listado de los parámetros que recibe el programa, indicando qué parámetros son obligatorios y cuales son opcionales, así como también ejemplos de comandos para ejecutarlo
Listado de los autores del proyecto
-->

# ChequesITBANK

ChequesITBANK es un programa que permite consultar los cheques que tiene emitidos y depositados en sus cuentas un determinado cliente

## Dependencias

- Python3: https://www.python.org/downloads/

### Instalacion de las dependencias

Para instalar las dependencias en Windows ejecutar:

-

Para instalar las dependencias en Linux ejecutar:

-

## Ejecución del programa

- Al ejecutar el programa correr:
    python listado_chesques.py [Nombre de archivo] [DNI] [salida] [tipo cheque] [estado] [fecha inicio] [fecha fin]
- Ejemplo:
    python listado_chesques.py test.csv 44160039 csv DEPOSITADO PENDIENTE 10-06-2002 10-06-2022
Los parámetros obligatorios son: nombreDeArchivo, dniBuscado, salida, tipoCheque
Los parámetros opcionales son: estado y rango

## Autores del proyecto

- Ian Dalton
- Santiago Javier Ance
- Jose Miserendino
- Ignacio Brandan
