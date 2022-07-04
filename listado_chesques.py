import csv
import datetime

nombreDeArchivo = "test.csv"
dniBuscado = 1617591371
salida = "Pantalla"
tipoCheque = "Emitido"
estado = "APROBADO"
rango = "03-06-2020:04-07-2022"


def extractorDeDatos(archivo):
    def valor(matriz):
        nuevaMatriz = []
        for fila in matriz:
            for letra in fila['Valor']:
                monto = ""
                if letra == ",":
                    monto += "."
                else:
                    monto += letra

            nuevaMatriz.append([
                int(fila["NroCheque"]),
                int(fila['CodigoBanco']),
                int(fila['CodigoScurusal']),
                int(fila['NumeroCuentaOrigen']),
                int(fila['NumeroCuentaDestino']),
                float(monto),
                int(fila['FechaOrigen']),
                int(fila['FechaPago']),
                int(fila['DNI']),
                fila['Tipo'],
                fila['Estado']])

        return nuevaMatriz

    datos = open(archivo, "r")
    matriz = csv.DictReader(datos)
    matriz = valor(matriz)
    datos.close()

    return matriz


def filtro(matriz, dni, tipo, estado, fechas):
    matriz = revisarDNI(matriz, dni)
    if matriz[0] == "Error 1" or matriz[0] == "Error 0":
        return matriz
    inicio, fin = obtenerFechas(fechas)
    matriz = revisarFechas(matriz, inicio, fin)
    if len(matriz) == 0:
        return["Error 2"]
    matriz = revisarEstado(matriz, estado)
    if len(matriz) == 0:
        return["Error 3"]
    return matriz


def obtenerFechas(criterio):
    dia = ""
    mes = ""
    anio = ""
    temp = ""
    inicio = 0
    fin = 0
    for char in criterio:
        if char != ":":

            if char != "-":
                temp += char

            else:
                if dia == "":
                    dia = int(temp)
                elif mes == "":
                    mes = int(temp)
                temp = ""
        else:
            anio = int(temp)
            if inicio == 0:
                inicio = datetime.datetime(anio, mes, dia, 0, 0)
            dia, mes, anio, temp = "", "", "", ""

    anio = int(temp)
    fin = datetime.datetime(anio, mes, dia, 0, 0)
    return inicio, fin


def revisarDNI(matriz, dni):
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


def revisarFechas(matriz, inicio, fin):
    nuevaMatriz = []
    for valor in matriz:
        fechaOr = datetime.datetime.fromtimestamp(valor[7])
        fechaPa = datetime.datetime.fromtimestamp(valor[8])
        if inicio < fechaOr and fechaPa < fin:
            nuevaMatriz.append(valor)
    matriz = nuevaMatriz
    return matriz


def revisarEstado(matriz, estado):
    n = 10
    nuevaMatriz = []

    for i in range(len(matriz)):
        if matriz[i][n] == estado:
            nuevaMatriz.append(matriz[i])

    if len(nuevaMatriz) == 0:
        return matriz

    else:
        return nuevaMatriz


def printeador(matriz):

    return


def guardarCSV(matriz, dni):

    return


def main():
    listaCompleta = extractorDeDatos(nombreDeArchivo)

    listaReducida = filtro(listaCompleta, int(
        dniBuscado), tipoCheque.upper(), estado.upper(), rango)
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
        guardarCSV(listaReducida, dniBuscado)


main()
