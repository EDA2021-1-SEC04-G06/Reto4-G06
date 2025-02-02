﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
import sys
import controller
import threading
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicilizar y cargar información en el catálogo")
    print("2- Requerimiento 1")
    print("3- Requerimiento 2")
    print("4- Requerimiento 3")
    print("5- Requerimiento 4")
    print("6- Requerimiento 5")
    print("7- Requerimiento 6")
    print("8- Requerimiento 7")
    print("0- Salir")
    print("*******************************************")
catalog = None


def respuestaxd(listita):
    for l in lt.iterator(listita):
        print('Desde: ' + str(l['vertexA']) + "      Hasta: " + str(l['vertexB']))
        print('Lo cual mide ' + str(l['weight']))

"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("Inicializando .... \n")
            catalog = controller.iniciar()
            print("Cargando información de los archivos ....\n")
            controller.loadArchivos(catalog)
            print("Total landing points: " + str(controller.totalVer(catalog)))
            print("Total conexiones entre landing points: " + str(controller.totalConnections(catalog)))
            print("Total paises: " + str(controller.totalPaises(catalog)))
            primero = controller.primerVer(catalog)
            print("Primer landing point: ")
            print("     Identificador: " + str(primero['landing_point_id']))
            print("     Nombre: " + str(primero['name']))
            print("     Latitud: " + str(primero['latitude']))
            print("     Longitud: " + str(primero['longitude']))
            print("Ultimo pais cargado: ")
            pais = controller.primerPai(catalog)
            print("     Nombre: " + str(pais['CountryName']))
            print("     Poblacion: " + str(pais['Population']))
            print("     Usuarios de internet: " + str(pais['Internet users']))
            print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
        elif int(inputs[0]) == 2:
            point1 = input('Ingrese el primer Landing Point (ej Redondo Beach): ')
            point2 = input('Ingrese el segundo Landing Point (ej Vung Tau): ')
            res = controller.requerimiento1(catalog, point1, point2)
            print('El total de clusters presentes es: ' + str(res[0]))
            if res[1]:
                print('Los dos landing points estan en el mismo cluster ')
            else:
                print('Los dos landing points noooo estan en el mismo cluster')
        elif int(inputs[0]) == 3:
            resp = controller.requerimiento2(catalog)
            for r in lt.iterator(resp):
                print("Nombre: " + str(r[1]))
                print("País:" + str(r[2]).split(',')[1])
                print("Identificador: " + str(r[0]))
                print("Total cables conectados: " + str(r[3])  )
                print("\n")
        elif int(inputs[0]) == 4:
            pais1 = input('Ingrese el primer Pais (ej Colombia): ')
            pais2 = input('Ingrese el segundo Pais (ej Indonesia): ')
            puesta = controller.requerimiento3(catalog, pais1, pais2)
            print("Ruta mas corta: ")
            respuestaxd(puesta[0])
            print('Total distancia de la ruta ' + str(puesta[1]) + ' Km')
        elif int(inputs[0]) == 5:
            r = controller.requerimiento4(catalog)
            print('Numero de nodos conectados a la red de expancion minima: ' + str(r[0]))
            print('Costo totaal de la red de expancion minima: ' + str(r[1]) + ' Km')
            print('Rama mas larga: ')
            respuestaxd(r[2])
        elif int(inputs[0]) == 6:
            poin = input('Ingrese el Nombre del landing point: ')
            rere = controller.requerimiento5(catalog, poin)
            print('Afecta un total de: ' + str(lt.size(rere)) + ' pises')
            print('Lista paises')
            for p in lt.iterator(rere):
                print(str(p[0]))
        elif int(inputs[0]) == 7:
            pass

        elif int(inputs[0]) == 8:
            pass

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
