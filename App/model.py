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


from DISClib.DataStructures.chaininghashtable import get
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
                'points': None,
                'points2': None,
                'compo': None
                }
    catalog['points'] = mp.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareVerIds)

    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=5000,
                                            comparefunction=compareVerIds)
    catalog['countries'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['points2'] = lt.newList(datastructure='ARRAY_LIST')
    return catalog

# Funciones para agregar informacion al catalogo


def addCount(catalog, count):
    lt.addLast(catalog['countries'], count)
    addPais(catalog, count)


def addPoint(catalog, point):
    lt.addLast(catalog['points2'], point)
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
        addPointcable(catalog, idorigen, cable)
        addPointcable(catalog, idedestino, cable)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addPointConne')


def addmismoId(catalog):
    try:
        for i in lt.iterator(gr.vertices(catalog['connections'])):
            idd1 = i.split("-", 1)
            idorigen = idd1[0]
            for j in lt.iterator(gr.vertices(catalog['connections'])):
                idd2 = j.split("-", 1)
                if idd1[1] != idd2[1] and idd1[0] == idd2[0]:
                    idedestino = idd2[0]
                    cable1 = idd1[1]
                    cable2 = idd2[1]
                    origen = formatVertex(idorigen, cable1)
                    destino = formatVertex(idedestino, cable2)
                    distancia = 0.1
                    addVer(catalog, origen)
                    addVer(catalog, destino)
                    addConne(catalog, origen, destino, distancia)
                    addPointcable(catalog, idorigen, cable1)
                    addPointcable(catalog, idedestino, cable2)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addmismoId')


def addPais(catalog, pais):
    try:
        if pais['CapitalName'] != '':
            idorigen = pais['CapitalName'].replace("-", "").lower()
        else:
            idorigen = pais['CountryName'].replace("-", "").lower()
        loc1 = (float(pais['CapitalLatitude']), float(pais['CapitalLongitude']))
        distancia = -1
        destino = None
        des = None
        for j in lt.iterator(gr.vertices(catalog['connections'])):
            idd = j.split("-", 1)
            ll = mp.get(catalog['points'], idd[0])
            i = ll['value']
            loc2 = (float(i['latitude']), float(i['longitude']))
            d = hs.haversine(loc1, loc2)
            if distancia == -1:
                distancia = d
                des = idd
                destino = i
            elif distancia > d:
                distancia = d
                des = idd
                destino = i
        idedestino = destino['landing_point_id']
        cable = des[1]
        point = {'landing_point_id': idorigen, 'id': str(idorigen) + '-' + pais['CountryName'], 'name': str(idorigen) + ', ' + pais['CountryName'], 'latitude': pais['CapitalLatitude'], 'longitude': pais['CapitalLongitude']}
        addPoint(catalog, point)
        origen = formatVertex(idorigen, pais['CountryCode'])
        destino = formatVertex(idedestino, cable)
        addVer(catalog, origen)
        addVer(catalog, destino)
        addConne(catalog, origen, destino, distancia)
        addPointcable(catalog, idorigen, pais['CountryCode'])
        addPointcable(catalog, idedestino, cable)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addPais')

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


def totalVer(catalog):
    return gr.numVertices(catalog['connections'])


def totalConnections(catalog):

    return gr.numEdges(catalog['connections'])


def primerVer(catalog):
    pri = lt.firstElement(catalog['points2'])
    return pri


def primerPai(catalog):
    return lt.lastElement(catalog['countries'])


def totalPaises(catalog):
    return lt.size(catalog['countries'])
# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareVerIds(ver, keyvaluever):
    
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


def requerimiento1(catalog, point1, point2):
    catalog['compo'] = scc.KosarajuSCC(catalog['connections'])
    k = 1
    g = 1
    tr1 = False
    tr2 = False
    while k <= lt.size(gr.vertices(catalog['connections'])) and not tr1:
        j = lt.getElement(gr.vertices(catalog['connections']), k)
        idd1 = j.split("-", 1)
        ll1 = mp.get(catalog['points'], idd1[0])
        name1 = ll1['value']['name']
        if point1.lower() in name1.lower():
            ver1 = j
            tr1 = True
        k += 1
    while g <= lt.size(gr.vertices(catalog['connections'])) and not tr2:
        i = lt.getElement(gr.vertices(catalog['connections']), g)
        idd2 = i.split("-", 1)
        ll2 = mp.get(catalog['points'], idd2[0])
        name2 = ll2['value']['name']
        if point2.lower() in name2.lower():
            ver2 = i
            tr2 = True
        g += 1
    con = scc.stronglyConnected(catalog['compo'], ver1, ver2)
    return scc.connectedComponents(catalog['compo']), con


def requerimiento2(catalog):
    catalog['compo'] = scc.KosarajuSCC(catalog['connections'])
    listaa = lt.newList('ARRAY_LIST')
    for j in lt.iterator(gr.vertices(catalog['connections'])):
        nu = scc.sccCount(catalog['connections'], catalog['compo'], j)
        lt.addLast(listaa, lt.size(nu))
    nueva = sa.sort(listaa, compareIds)
    return nueva

