"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización 

def iniciar():
    catalog = model.newcatalog()
    return catalog

# Funciones para la carga de datos

def loadArchivos(catalog):
    loadPoints(catalog)
    loadConnec(catalog)
    loadCount(catalog)
    return catalog


def loadPoints(catalog):
    pointfile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(pointfile, encoding='utf-8'))
    for point in input_file:
        model.addPoint(catalog, point)


def loadConnec(catalog):
    connefile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(connefile, encoding='utf-8-sig'))
    for conne in input_file:
        model.addPointConne(catalog, conne)


def loadCount(catalog):
    countfile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(countfile, encoding='utf-8-sig'))
    for count in input_file:
        model.addCount(catalog, count)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def totalVer(catalog):
    return model.totalVer(catalog)


def totalConnections(catalog):
    return model.totalConnections(catalog)


def primerVer(catalog):
    return model.primerVer(catalog)


def primerPai(catalog):
    return model.primerPai(catalog)