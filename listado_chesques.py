import csv
import datetime

nombreDeArchivo = "test.csv"
dniBuscado = "1617591371"
salida = "Pantalla"


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
    matrizNueva = []

    return matrizNueva  # Si hay un error matriz nueva devuelve ["Error",Nro de cheque repetido]


def printeador(matriz):

    return


def guardarCSV(matriz,dni):

    return


def main():
    listaCompleta = extractorDeDatos(nombreDeArchivo)

    listaReducida = filtro(listaCompleta,dniBuscado)
    if listaReducida[0] == "Error":
        print("ERROR: Se repite el siguiente cheque del DNI",dniBuscado,":",listaReducida[1])
        return  # Se corta el codigo aca y no se sigue

    if salida.upper() == "PANTALLA":
        printeador(listaReducida)
    elif salida.upper() == "CSV":
        guardarCSV(listaReducida,dniBuscado)


main()
