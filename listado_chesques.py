import csv
import datetime
import sys

nombreDeArchivo = "test.csv"
dniBuscado = 1617591371
salida = "csv"


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

    datos = open(archivo,"r")
    matriz = csv.DictReader(datos)
    matriz = valor(matriz)
    datos.close()

    return matriz


def filtro(matriz,dni):
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


def printeador(listaReducida):
    for i in range(len(listaReducida)):
        print(listaReducida[i])
    return


def guardarCSV(matriz,dni):
    now = datetime.datetime.now()
    with open(now.strftime('%Y-%m-%dT%H:%M:%S.csv'), "w") as f:
        f.write(matriz)
    return


def main():
    listaCompleta = extractorDeDatos(nombreDeArchivo)
    
    listaReducida = filtro(listaCompleta,int(dniBuscado))
    
    if listaReducida[0] == "Error 0":
        print("ERROR: Se repiten uno o mas cheques del DNI:",dniBuscado)
        return  # Se corta el codigo aca y no se sigue
    elif listaReducida[0] == "Error 1":
        print("ERROR: No existen cheques para el DNI:",dniBuscado)
        return

    if salida.upper() == "PANTALLA":
        printeador(listaReducida)
    elif salida.upper() == "CSV":
        guardarCSV(listaReducida,dniBuscado)


if __name__ == "__main__":
    main()
