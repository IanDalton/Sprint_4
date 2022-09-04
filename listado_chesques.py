'''
* El programa no recibe por linea de comando los argumentos, sino que se encuentran hardcodeados en el programa.

Debieran haber hecho uso de sys.argv para recuperar los argumentos

* El código no sigue la convención de snake case para nombrar métodos y variables

* ¿Por qué se define una función dentro de la función extractor_de_datos? Eso es confuso

* No entiendo esto:

for fila in matriz:

for letra in fila['Valor']:

monto = ""

if letra == ",":

monto += "."

else:

monto += letra

* La forma de nombrar las variables no es correcta, que es n2 en la función revisar_DNI?

* ¿Por que la funcion revisar_DNI returna una lista con un string que dice Error 1 o Error 0? Que significa cada error? No sería mejor retornar un

un entero que este definido en una constante para que sea mas claro?

* El return al final de guardar_CSV está demás

* La funcion guardar_CSV recibe un parametro dni que no se usa

* La funcion guardar_CSV tiene hardcodeado el header del archivo csv

* ¿Por qué convierten el número de cheque a entero? En el archivo de prueba el número de cheque figura como 0001, al convertir eso a int, hace que el numero quede como 1 pues le remueve los ceros delanteros

Eso hace que cuando escriban el CSV de salida la fila que se guarda en el CSV tenga un numero de cheque distinto 1 vs 0001. Se supone que el archivo CSV que ustedes guardan tiene que ser un subconjunto de los datos

que hay en el archivo de entrada test.csv. NO pueden modificarse los datos

* Esto mismo sucede con el valor, que lo convierten a float. ¿Cuál es el sentido de hacer esas conversiones si no están realizando ningun tipo de validacion

ni chequeo respecto al valor? Al convertirlo a float se le agrega el punto decimal lo cual modifica el dato original que se tiene en el archivo de entrada

* Segun los parametros que ustedes hardcodearon en el programa y dado el archivo test.csv que tienen subido a su repositorio, al ejecutarlo debiera dar como resultado la siguiente linea:

0011,1,12,23123132,12312312,5000,1617591371,1617591371,1617591371,EMITIDO,APROBADO

Sin embargo, en el archivo de salida da como resultado la siguiente linea:

11,1,12,23123132,12312312,0.0,1617591371,1617591371,1617591371,EMITIDO,APROBADO

Se está mostrando como 0.0 el campo valor.

'''

import csv
import datetime
from re import L
import sys

print(sys.argv)
nombreDeArchivo = sys.argv[1]
dniBuscado = sys.argv[2]
salida = sys.argv[3]
tipoCheque = sys.argv[4]
try:
    estado = sys.argv[5]
except:
    estado = None
try:
    rango = sys.argv[6]+':'+sys.argv[7]
except:
    rango = None


def extractor_de_datos(archivo):
    def valor(matriz):
        nuevaMatriz = []
        for fila in matriz:
            nuevaMatriz.append([
                fila["NroCheque"],
                fila['CodigoBanco'],
                fila['CodigoScurusal'],
                fila['NumeroCuentaOrigen'],
                fila['NumeroCuentaDestino'],
                fila['Valor'],
                fila['FechaOrigen'],
                fila['FechaPago'],
                fila['DNI'],
                fila['Tipo'],
                fila['Estado']])

        return nuevaMatriz

    datos = open(archivo, "r")
    matriz = csv.DictReader(datos)
    matriz = valor(matriz)
    datos.close()

    return matriz


def filtro(matriz, dni, tipo, estado, fechas):
    matriz = revisar_DNI(matriz, dni)
    if matriz[0] == "Error 1" or matriz[0] == "Error 0":
        return matriz
    if fechas:
        inicio, fin = obtener_fechas(fechas)
        matriz = revisar_fechas(matriz, inicio, fin)
        if len(matriz) == 0:
            return ["Error 2"]
    if estado:
        matriz = revisar_estado(matriz, estado)
        if len(matriz) == 0:
            return ["Error 3"]
    matriz = revisar_tipo(matriz, tipo)
    if len(matriz) == 0:
        return ["Error 4"]
    return matriz


def obtener_fechas(criterio):

    fechas = criterio.split(':')
    print(fechas)
    fecha_desde = datetime.datetime.strptime(fechas[0], '%d-%m-%Y')
    fecha_hasta = datetime.datetime.strptime(fechas[1], '%d-%m-%Y')
    return fecha_desde, fecha_hasta


def revisar_DNI(matriz, dni):
    n = 8
    n2 = 0
    nrosChq = []
    matrizNueva = []

    for i in range(len(matriz)):
        if matriz[i][n] == dni:
            nrosChq.append(matriz[i][n2])
            matrizNueva.append(matriz[i])

    if len(nrosChq) == 0:
        return ["Error 1"]

    nrosChqSinRepetir = set(nrosChq)
    if len(nrosChq) != len(nrosChqSinRepetir):
        return ["Error 0"]
    return matrizNueva


def revisar_fechas(matriz, inicio, fin):
    nuevaMatriz = []
    for valor in matriz:
        fechaOr = datetime.datetime.fromtimestamp(int(valor[7]))
        fechaPa = datetime.datetime.fromtimestamp(int(valor[8]))
        if inicio < fechaOr and fechaPa < fin:
            nuevaMatriz.append(valor)
    matriz = nuevaMatriz
    return matriz


def revisar_estado(matriz, estado):
    n = 10
    nuevaMatriz = []

    for i in range(len(matriz)):
        if matriz[i][n] == estado:
            nuevaMatriz.append(matriz[i])

    if len(nuevaMatriz) == 0:
        return []

    else:
        return nuevaMatriz


def printeador(listaReducida):
    for i in range(len(listaReducida)):
        print(listaReducida[i])
    return


def revisar_tipo(matriz, tipo):
    n = 9
    nuevaMatriz = []

    for i in range(len(matriz)):
        if matriz[i][n] == tipo:
            nuevaMatriz.append(matriz[i])

    if len(nuevaMatriz) == 0:
        return []

    else:
        return nuevaMatriz


def guardar_CSV(matriz, dni):
    now = datetime.datetime.now()
    with open(now.strftime('%Y-%m-%dT%H-%M-%S.csv'), "w") as f:
        f.write("NroCheque,CodigoBanco,CodigoScurusal,NumeroCuentaOrigen,NumeroCuentaDestino,Valor,FechaOrigen,FechaPago,DNI,Tipo,Estado\n")
        for linea in matriz:
            i = len(linea)
            for palabra in linea:
                i -= 1
                f.write(str(palabra))
                if i != 0:
                    f.write(",")
            f.write("\n")
    return


def main():
    listaCompleta = extractor_de_datos(nombreDeArchivo)

    listaReducida = filtro(listaCompleta,
                           dniBuscado, tipoCheque, estado, rango)
    if listaReducida[0] == "Error 0":
        print("ERROR: Se repiten uno o mas cheques del DNI:", dniBuscado)
        return  # Se corta el codigo aca y no se sigue
    elif listaReducida[0] == "Error 1":
        print("ERROR: No existen cheques para el DNI:", dniBuscado)
        return
    elif listaReducida[0] == "Error 2":
        print("ERROR: No existen cheques entre las fechas",
              rango, "para el DNI:", dniBuscado)
        return
    elif listaReducida[0] == "Error 3":
        print("ERROR: No existen cheques con el estado",
              estado, "para el DNI:", dniBuscado)
        return

    if salida.upper() == "PANTALLA":
        printeador(listaReducida)
    elif salida.upper() == "CSV":
        guardar_CSV(listaReducida, dniBuscado)


main()
