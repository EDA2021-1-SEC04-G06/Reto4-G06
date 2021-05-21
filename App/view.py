"""
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
    print("9- Requerimiento 8")
    print("0- Salir")
    print("*******************************************")
catalog = None

"""
Menu principal
"""
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
        print("Total paises: ")
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
    elif int(inputs[0]) == 2:
        pass

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        pass

    elif int(inputs[0]) == 8:
        pass

    elif int(inputs[0]) == 9:
        pass

    else:
        sys.exit(0)
sys.exit(0)
