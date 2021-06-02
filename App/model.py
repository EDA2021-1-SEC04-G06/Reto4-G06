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


from numpy import info
from DISClib.DataStructures.arraylist import iterator, subList
from DISClib.DataStructures.chaininghashtable import get
import config as cf
from DISClib.ADT.graph import gr, vertices
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import haversine as hs
import folium


# hs.haversine(loc1,loc2,unit=Unit.METERS)
assert cf

# Construccion de modelos


def newcatalog():
    catalog = { 
                'countries': None,
                'connections': None,
                'points': None,
                'points2': None,
                'compo': None,
                'rutas': None,
                'mst': None
                }
    catalog['points'] = mp.newMap(numelements=4000,
                                     maptype='PROBING',
                                     comparefunction=compareVerIds)

    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=20000,
                                            comparefunction=compareVerIds)
    
    catalog['mst'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=20000,
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
            distancia = 1000
        else:
            distancia = float(coneccion['cable_length'].replace(',','').strip(' km'))
        addVer(catalog, origen)
        addVer(catalog, destino)
        addConne(catalog, origen, destino, distancia)
        addConne(catalog, destino, origen, distancia)
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
                if idd1[0] == idd2[0]:
                    idedestino = idd2[0]
                    cable1 = idd1[1]
                    cable2 = idd2[1]
                    origen = formatVertex(idorigen, cable1)
                    destino = formatVertex(idedestino, cable2)
                    distancia = 0.1
                    addVer(catalog, origen)
                    addVer(catalog, destino)
                    addConne(catalog, origen, destino, distancia)
                    addConne(catalog, destino, origen, distancia)
                    addPointcable(catalog, idorigen, cable2)
                    addPointcable(catalog, idedestino, cable1)
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
            if distancia == -1 and len(idd[1]) > 2:
                distancia = d
                des = idd
                destino = i
            elif distancia > d and len(idd[1]) > 2:
                distancia = d
                des = idd
                destino = i
        idedestino = destino['landing_point_id']
        origen = formatVertex(idorigen, pais['CountryCode'])
        addVer(catalog, origen)
        point = {'landing_point_id': idorigen, 'id': str(idorigen) + '-' + pais['CountryName'], 'name': str(idorigen) + ', ' + pais['CountryName'], 'latitude': pais['CapitalLatitude'], 'longitude': pais['CapitalLongitude']}
        addPoint(catalog, point)
        for h in lt.iterator(gr.vertices(catalog['connections'])):
            hdd = h.split("-", 1)
            if des[0] == hdd[0]:
                cable = hdd[1]
                destino = formatVertex(idedestino, cable) 
                addVer(catalog, destino)
                addConne(catalog, origen, destino, distancia)
                addConne(catalog, destino, origen, distancia)
                addPointcable(catalog, idorigen, pais['CountryCode'])
                addPointcable(catalog, idedestino, cable)
                addPointcable(catalog, idedestino, pais['CountryCode'])
                addPointcable(catalog, idorigen, cable)
        addMismoPais(catalog, pais)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addPais')


def addMismoPais(catalog, pais):
    if pais['CapitalName'] != '':
        idorigen = pais['CapitalName'].replace("-", "").lower()
    else:
        idorigen = pais['CountryName'].replace("-", "").lower()
    origen = formatVertex(idorigen, pais['CountryCode'])
    loc1 = (float(pais['CapitalLatitude']), float(pais['CapitalLongitude']))
    for j in lt.iterator(gr.vertices(catalog['connections'])):
        coco = j.split("-", 1)
        pa = mp.get(catalog['points'], coco[0])
        if pais['CountryName'].lower() in pa['value']['name'].lower():
            loc2 = (float(pa['value']['latitude']), float(pa['value']['longitude']))
            distancia = hs.haversine(loc1, loc2)
            addVer(catalog, j)
            addConne(catalog, origen, j, distancia)
            addConne(catalog, j, origen, distancia)
            addPointcable(catalog, idorigen, pais['CountryCode'])
            addPointcable(catalog, coco[0], coco[1])
            addPointcable(catalog, coco[0], pais['CountryCode'])
            addPointcable(catalog, idorigen, coco[1])
    return catalog


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

def addVerMst(catalog, pointid):
    try:
        if not gr.containsVertex(catalog['mst'], pointid):
            gr.insertVertex(catalog['mst'], pointid)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addVerMst')


def addConneMst(catalog, origen, destino, distancia):
    edge = gr.getEdge(catalog['mst'], origen, destino)
    if edge is None:
        gr.addEdge(catalog['mst'], origen, destino, distancia)
    return catalog


def addPointConneMst(catalog, ver1, ver2, distancia):
    try:
        origen = ver1
        destino = ver2
        addVerMst(catalog, origen)
        addVerMst(catalog, destino)
        addConneMst(catalog, origen, destino, distancia)
        addConneMst(catalog, destino, origen, distancia)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addPointConneMst')


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

def kmdes(pa1, pa2):
    if pa1[1] == pa2[1]:
        return 0
    elif pa1[1] < pa2[1]:
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


def comparecone(c1, c2):
    if c1[3] > c2[3]:
        return 1
    elif c1[3] == c2[3]:
        return 0
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
    requerimiento8(catalog)
    return scc.connectedComponents(catalog['compo']), con


def requerimiento2(catalog):
    verti = mp.keySet(catalog['points'])
    listaa = lt.newList('ARRAY_LIST')
    mayor = 0
    for v in lt.iterator(verti):
        c = mp.get(catalog['points'], v)['value']
        total = lt.size(c['cables'])
        lt.addLast(listaa, (c['landing_point_id'], c['id'], c['name'], total, c['cables']))
        if total > mayor: 
            mayor = total
            primis = v
    listaa = listaa.copy()
    final = sa.sort(listaa, comparecone)
    final2 = lt.subList(final, 1, 10)
    k = 1
    tr1 = False
    while k <= lt.size(gr.vertices(catalog['connections'])) and not tr1:
        j = lt.getElement(gr.vertices(catalog['connections']), k)
        idd1 = j.split("-", 1)
        ll1 = mp.get(catalog['points'], idd1[0])
        name1 = ll1['value']['landing_point_id']
        if primis == name1:
            ver1 = j
            tr1 = True
        k += 1
    m = folium.Map(location=[4.6, -74.083333], tiles="Stamen Terrain")
    cv = ver1.split("-", 1)
    infov = mp.get(catalog['points'], cv[0])['value']
    folium.Marker([float(infov['latitude']),  float(infov['longitude'])], popup=str(infov['name'])).add_to(m)
    ad = gr.adjacents(catalog['connections'], ver1)
    for e in lt.iterator(ad):
        ce = e.split("-", 1)
        infoe = mp.get(catalog['points'], ce[0])['value']
        folium.Marker([float(infoe['latitude']),  float(infoe['longitude'])], popup=str(infoe['name'])).add_to(m)
        folium.PolyLine(locations=[(float(infov['latitude']), float(infov['longitude'])), (float(infoe['latitude']), float(infoe['longitude']))], tooltip=str(cv[1])).add_to(m)
    m.save('mapa_req2.html')
    return final2


def requerimiento3(catalog, pais1, pais2):
    k = 1
    g = 1
    tr1 = False
    tr2 = False
    e1 = None
    while k <= lt.size(catalog['countries']) and not tr1:
        p = lt.getElement(catalog['countries'], k)
        if p['CountryName'].lower() in pais1.lower():
            tr1 = True
            e1 = p
        k += 1
    e2 = None
    while g <= lt.size(catalog['countries']) and not tr2:
        f = lt.getElement(catalog['countries'], g)
        if f['CountryName'].lower() in pais2.lower():
            tr2 = True
            e2 = f
        g += 1
    pa1 = formatVertex(e1['CapitalName'].replace("-", "").lower(), e1['CountryCode'])
    pa2 = formatVertex(e2['CapitalName'].replace("-", "").lower(), e2['CountryCode'])
    catalog['rutas'] = djk.Dijkstra(catalog['connections'], pa1)
    ruta = djk.pathTo(catalog['rutas'], pa2)
    distancia = djk.distTo(catalog['rutas'],  pa2)

    m = folium.Map(location=[4.6, -74.083333], tiles="Stamen Terrain")
    ad = ruta
    for e in lt.iterator(ad):
        cv = e['vertexA'].split("-", 1)
        
        ce = e['vertexB'].split("-", 1)
        infov = mp.get(catalog['points'], cv[0])['value']
        infoe = mp.get(catalog['points'], ce[0])['value']
        folium.Marker([float(infov['latitude']),  float(infov['longitude'])], popup=str(infov['name'])).add_to(m)
        folium.Marker([float(infoe['latitude']),  float(infoe['longitude'])], popup=str(infov['name'])).add_to(m)
        folium.PolyLine(locations=[(float(infov['latitude']), float(infov['longitude'])), (float(infoe['latitude']), float(infoe['longitude']))], tooltip=str(cv[1])).add_to(m)

    m.save('mapa_req3.html')
    return ruta, distancia


def requerimiento4(catalog):
    pri = prim.PrimMST(catalog['connections'])
    peso = prim.weightMST(catalog['connections'], pri)
    mst = prim.edgesMST(catalog['connections'], pri)['mst']
    m = folium.Map(location=[4.6, -74.083333], tiles="Stamen Terrain")
    for st in lt.iterator(mst):
        cv = st['vertexA'].split("-", 1)
        ce = st['vertexB'].split("-", 1)
        infov = mp.get(catalog['points'], cv[0])['value']
        infoe = mp.get(catalog['points'], ce[0])['value']
        addPointConneMst(catalog, st['vertexA'], st['vertexB'], st['weight'])
        folium.PolyLine(locations=[(float(infov['latitude']), float(infov['longitude'])), (float(infoe['latitude']), float(infoe['longitude']))], tooltip=str(cv[1])).add_to(m)
        folium.Marker([float(infov['latitude']),  float(infov['longitude'])], popup=str(infov['name'])).add_to(m)
        folium.Marker([float(infoe['latitude']),  float(infoe['longitude'])], popup=str(infoe['name'])).add_to(m)
    m.save('mapa_req4.html')
    gramst = catalog['mst']
    vert = gr.vertices(gramst)
    num = lt.size(vert)
    primero = lt.firstElement(vert)
    mayor = 0
    camino = None
    dijta = djk.Dijkstra(catalog['mst'], primero)
    for v in lt.iterator(vert):
        ruta = djk.pathTo(dijta, v)
        x = lt.size(ruta)
        if x > mayor:
            mayor = x
            camino = ruta
    return num, peso, camino


def requerimiento5(catalog, poin):
    paisesf = lt.newList(datastructure='ARRAY_LIST')
    k = 1
    tr1 = False
    while k <= lt.size(gr.vertices(catalog['connections'])) and not tr1:
        j = lt.getElement(gr.vertices(catalog['connections']), k)
        idd1 = j.split("-", 1)
        ll1 = mp.get(catalog['points'], idd1[0])
        name1 = ll1['value']['name']
        if poin.lower() in name1.lower():
            ver1 = ll1
            tr1 = True
        k += 1
    ca = ver1['value']
    tamca = lt.size(ca['cables']) 
    for coun in lt.iterator(catalog['countries']):
        if coun['CapitalName'] != '':
            cap = coun['CapitalName'].replace("-", "").lower()
        else:
            cap = coun['CountryName'].replace("-", "").lower()
        tr2 = False
        ll2 = mp.get(catalog['points'], cap)['value']
        g = 1
        while g <= tamca and not tr2:
            c = lt.getElement(ca['cables'], g)
            if lt.isPresent(ll2['cables'], c) != 0:
                tr2 = True
                distanci = hs.haversine((float(ca['latitude']),float(ca['longitude'])), (float(coun['CapitalLatitude']), float(coun['CapitalLongitude'])))
                lt.addLast(paisesf, (coun['CountryName'], distanci, cap, c))
            g += 1
    paisesf = paisesf.copy()
    ordee = sa.sort(paisesf, kmdes)
    
    m = folium.Map(location=[4.6, -74.083333], tiles="Stamen Terrain")
    infov = ca
    folium.Marker([float(infov['latitude']),  float(infov['longitude'])], popup=str(infov['name'])).add_to(m)
    ad = ordee
    for e in lt.iterator(ad):
        ce = e[2]
        infoe = mp.get(catalog['points'], ce)['value']
        folium.Marker([float(infoe['latitude']),  float(infoe['longitude'])], popup=str(infoe['name'])).add_to(m)
        folium.PolyLine(locations=[(float(infov['latitude']), float(infov['longitude'])), (float(infoe['latitude']), float(infoe['longitude']))], tooltip=str(e[3])).add_to(m)
    m.save('mapa_req5.html')
    return ordee


def requerimiento8(catalog):
    m = folium.Map(location=[4.6, -74.083333], tiles="Stamen Terrain")
    vertice = gr.vertices(catalog['connections'])
    for v in lt.iterator(vertice):
        cv = v.split("-", 1)
        infov = mp.get(catalog['points'], cv[0])['value']
        folium.Marker([float(infov['latitude']),  float(infov['longitude'])], popup=str(infov['name'])).add_to(m)
        ad = gr.adjacents(catalog['connections'], v)
        for e in lt.iterator(ad):
            ce = e.split("-", 1)
            infoe = mp.get(catalog['points'], ce[0])['value']
            folium.PolyLine(locations=[(float(infov['latitude']), float(infov['longitude'])), (float(infoe['latitude']), float(infoe['longitude']))], tooltip=str(cv[1])).add_to(m)

    m.save('mapa_req1.html')
    return m
    