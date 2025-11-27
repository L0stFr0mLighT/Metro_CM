from dataclasses import dataclass, field
from networkx import Graph, astar_path, NetworkXNoPath

from common.estacion import Estacion, Linea, Conexion, Transbordo
from motor.mapa import Mapa

@dataclass
class Grafo:
    """
    Encapsula el grafo que modela la red.

    Los vertices del grafo seran tuplas de la forma (Estacion, Linea | None)
    Si el segundo miembro de la tupla es None, simboliza la entrada de la estacion.
    Esto es util para las estaciones con transbordo, que no sabemos si el usuario esta
    en (est, L_1) o en (est, L_3), por ejemplo.

    Las aristas son las conexiones entre estaciones a traves de una linea.
    """
    grafo: Graph = Graph()
    mapa: Mapa = field(default_factory=lambda : Mapa())

    destino_actual: Estacion | None = None

    def set_grafo(self, conexiones: list[Conexion], transbordos: list[Transbordo], mapa: Mapa):
        # TODO: Añadir mas datos aqui
        self.mapa = mapa
        for conexion in conexiones:
            # Añado las estaciones "generales"
            self.grafo.add_edge((conexion.origen, None), (conexion.origen, conexion.linea))

            self.grafo.add_edge((conexion.dest, None), (conexion.dest, conexion.linea))

            self.grafo.add_edge((conexion.origen, conexion.linea), (conexion.dest, conexion.linea))
        
        for transbordo in transbordos:
            self.grafo.add_edge((transbordo.estacion, transbordo.linea1), (transbordo.estacion, transbordo.linea2))

    def calcular_peso(self, cnx_origen: tuple[Estacion, Linea | None], cnx_dest: tuple[Estacion, Linea | None], _attr) -> float | None:
        if cnx_origen[1] == None:
            return 0
        
        if cnx_dest[1] == None:
            if cnx_dest[0] == self.destino_actual:
                return 0
            return None
        
        if cnx_origen[0] == cnx_dest[0]:
            transb = self.mapa.buscar_transbordos(cnx_origen[0], cnx_origen[1], cnx_dest[1])
            if transb == None:
                print("ERROR: La clase Mapa no ha encontrado el transbordo !!")
                return None
            return transb.tiempo_trasbordo

        cnx = self.mapa.buscar_conexion(cnx_origen[0], cnx_dest[0])
        if cnx == None:
            print("ERROR: Hay una arista para la que la clase Mapa no tiene conexion !!")
            return None
        return cnx[1]

    def heuristica(self, origen: Estacion, meta: Estacion) -> float:
        VELOCIDAD_MEDIA = 33 * 1000 / 60 # m / min
        # Calculamos la distancia entre dos puntos (formula de Haversine simplificada)
        delta_x = origen.localizacion[0] - meta.localizacion[0]
        delta_y = origen.localizacion[1] - meta.localizacion[1]

        distancia = 69.1 * (((0.629 * (delta_x ** 2)) + (delta_y ** 2)) ** 0.5)
        return distancia / VELOCIDAD_MEDIA

    def calcular_camino_minimo(self, origen: str, dest: str) -> list[tuple[Estacion, Linea | None]] | None:
        self.destino_actual = None

        est_origen = self.mapa.buscar_por_nombre(origen)
        if est_origen == None:
            return None
        est_dest = self.mapa.buscar_por_nombre(dest)
        if est_dest == None:
            return None
        
        try:
            self.destino_actual = est_dest
            return astar_path(self.grafo, (est_origen, None), (est_dest, None), heuristic=lambda x, y : self.heuristica(x[0], y[0]), 
                              weight=self.calcular_peso)
        except(NetworkXNoPath):
            self.destino_actual = None
            return None
