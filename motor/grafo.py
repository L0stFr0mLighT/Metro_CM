from dataclasses import dataclass, field
from networkx import Graph, astar_path, NetworkXNoPath
from geopy.distance import distance

from common.estacion import Estacion, Linea, Conexion, Transbordo
from motor.mapa import Mapa

@dataclass
class Grafo:
    """
    Encapsula el grafo que modela la red.

    Los vertices del grafo seran tuplas de la forma (Estacion, Linea | None)
    Si el segundo miembro de la tupla es None, simboliza la entrada de la estacion.

    Las aristas son las conexiones entre estaciones a traves de una linea.
    """
    grafo: Graph = Graph()
    mapa: Mapa = field(default_factory=lambda : Mapa())

    # Estado temporal
    destino_actual: Estacion | None = None
    menos_transbordos: bool = False

    def set_grafo(self, conexiones: list[Conexion], transbordos: list[Transbordo], mapa: Mapa):

        # CONTEXTO: para resolver el problema de determinar en qué línea exacta de una
        # estación con transbordos debemos comenzar, creamos un nodo adicional para cada
        # estación (estación general), que representa la entrada a dicha estación.
        # Desde este nodo se puede acceder a cualquier línea que pase por la estación sin coste. 
        
        self.mapa = mapa
        for conexion in conexiones:

            # Añado las estaciones "generales"
            self.grafo.add_edge((conexion.origen, None), (conexion.origen, conexion.linea))
            self.grafo.add_edge((conexion.dest, None), (conexion.dest, conexion.linea))

            self.grafo.add_edge((conexion.origen, conexion.linea), (conexion.dest, conexion.linea))
        
        for transbordo in transbordos:
            self.grafo.add_edge((transbordo.estacion, transbordo.linea1), (transbordo.estacion, transbordo.linea2))

    def calcular_peso(self, cnx_origen: tuple[Estacion, Linea | None], cnx_dest: tuple[Estacion, Linea | None], _attr) -> float | None:
        """
        Calcula el coste de ir entre los dos vertices dados. Usado para NetworkX
        """
        M = 100 # Valor grande que se usará como penalizacion por transbordo

        # Entrada a una línea
        if cnx_origen[1] == None:
            assert cnx_dest[1] != None
            return 0 + cnx_dest[1].frecuencia / 2   # Empiezas el viaje
        
        # Salida a la entrada de estacion (solo en la estación destino)
        if cnx_dest[1] == None:
            if cnx_dest[0] == self.destino_actual:
                return 0
            return None
        
        # Transbordo entre líneas
        if cnx_origen[0] == cnx_dest[0]:
            transb = self.mapa.buscar_transbordos(cnx_origen[0], cnx_origen[1], cnx_dest[1])
            if transb == None:
                print("ERROR: La clase Mapa no ha encontrado el transbordo !!")
                return None
            tiempo_transb = transb.tiempo_trasbordo + cnx_dest[1].frecuencia / 2
            return tiempo_transb + M if self.menos_transbordos else tiempo_transb

        # Tramo de viaje normal entre estaciones
        cnx = self.mapa.buscar_conexion(cnx_origen[0], cnx_dest[0])
        if cnx == None:
            print("ERROR: Hay una arista para la que la clase Mapa no tiene conexion !!")
            return None
        return cnx[1]

    def heuristica(self, origen: Estacion, meta: Estacion) -> float:
        """
        Calcula la heuristica
        """
        VELOCIDAD_MEDIA = 33 / 60 # km / min
        # Calculamos la distancia entre dos puntos usando geopy
        distancia = distance(origen.localizacion, meta.localizacion).km
        return distancia / VELOCIDAD_MEDIA

    def calcular_camino_minimo(self, origen: str, dest: str, menos_transbordos: bool) -> list[tuple[Estacion, Linea | None]] | None:
        """
        Calcula el camino minimo usando A*
        """
        self.destino_actual = None
        self.menos_transbordos = menos_transbordos

        est_origen = self.mapa.buscar_por_nombre(origen)
        if est_origen == None:
            return None
        est_dest = self.mapa.buscar_por_nombre(dest)
        if est_dest == None:
            return None
        
        try:
            self.destino_actual = est_dest
            res = astar_path(self.grafo, (est_origen, None), (est_dest, None), heuristic=lambda x, y : self.heuristica(x[0], y[0]), 
                              weight=self.calcular_peso)
            self.destino_actual = None
            self.menos_transbordos = False
            return res
        except(NetworkXNoPath):
            self.destino_actual = None
            self.menos_transbordos = False
            return None
    
    def calcular_tiempo_camino(self, camino: list[tuple[Estacion, Linea | None]]) -> float:
        """
        Calcula el tiempo para recorrer el camino en minutos
        """
        res = 0
        for i in range(len(camino) - 1):
            coste = self.calcular_peso(camino[i], camino[i+1], None)
            res += 0 if coste == None else coste
        
        return res
    
    def estaciones_principales(self, camino: list[tuple[Estacion, Linea | None]]) -> list[tuple[Estacion, Linea | None]]:
        """
        Devuelve las estaciones principales del recorrido. Es decir, las estaciones origen y destino;
        asi como los transbordos
        """
        res = list()

        for i in range(len(camino) - 1):
            if camino[i][1] != camino[i+1][1]:
                res.append(camino[i])
                res.append(camino[i+1])

        return res
