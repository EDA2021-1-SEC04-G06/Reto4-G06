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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import haversine as hs
# hs.haversine(loc1,loc2,unit=Unit.METERS)
assert cf

# Construccion de modelos


def newcatalog():
    catalog = { 
                'countries': None,
                'connections': None,
                'points': None
                }
    catalog['points'] = mp.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareVerIds)

    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=5000,
                                            comparefunction=compareVerIds)       
    catalog['countries'] = lt.newList(datastructure='SINGLE_LINKED', cmpfunction = comparePais )    

    return catalog

# Funciones para agregar informacion al catalogo
def addPoint(catalog, point):
    point['cables'] = None
    mp.put(catalog['points'], point['landing_point_id'], point)

def addPointConne(catalog, coneccion):
    try:
        idorigen = coneccion['origin']
        idedestino = coneccion['destination']
        cable = coneccion['cable_id']
        origen = formatVertex(idorigen, cable)
        destino = formatVertex(idedestino, cable)
        if 'n.a.' in coneccion['cable_length']:
            distancia = 0.1
        else:
            distancia = float(coneccion['cable_length'].replace(',','').strip(' km'))
        addVer(catalog, origen)
        addVer(catalog, destino)
        addConne(catalog, origen, destino, distancia)
        addPointcable(catalog, idorigen,cable)
        addPointcable(catalog, idedestino,cable)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addPointConne')


def addVer(catalog, pointid):
    try:
        if not gr.containsVertex(catalog['connections'], pointid):
            gr.insertVertex(catalog['connections'], pointid)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addVer')


def addConne(catalog, origen, destino, distancia):
    edge = gr.getEdge(catalog['connections'], origen, destino)
    if edge is None:
        gr.addEdge(catalog['connections'], origen, destino, distancia)
    return catalog


def addPointcable(catalog, pointid, cable):
    dato = mp.get(catalog['points'], pointid)
    if dato['value']['cables'] is None:
        ltcables = lt.newList(cmpfunction=comparecables)
        lt.addLast(ltcables, cable)
        dato['value']['cables'] = ltcables
    else:
        if not lt.isPresent(dato['value']['cables'], cable):
            lt.addLast(dato['value']['cables'], cable)
    return catalog

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareVerIds(ver, keyvaluever):
    """
    Compara dos estaciones
    """
    code = keyvaluever['key']
    if (ver == code):
        return 0
    elif (ver > code):
        return 1
    else:
        return -1

def comparecables(cable1, cable2):
  
    if (cable1 == cable2):
        return 0
    elif (cable1 > cable2):
        return 1
    else:
        return -1

def comparePais(pais1, pais2):
    if (pais1['CountryName'] == pais2['CountryName']):
        return 0
    elif (pais1['CountryName'] > pais2['CountryName']):
        return 1
    else:
        return -1
def formatVertex(point, cable):
    
    name = point + '-' + cable
    return name
