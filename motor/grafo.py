from dataclasses import dataclass
from networkx import DiGraph

from common.estacion import Estacion, Linea, Conexion, Transbordo

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
    grafo: DiGraph = DiGraph()

    def set_grafo(self, conexiones: list[Conexion], transbordos: list[Transbordo]):
        # TODO: Añadir mas datos aqui
        for conexion in conexiones:
            # Añado las estaciones "generales"
            # TODO: El grafo debe ser dirigido?
            self.grafo.add_edge((conexion.origen, None), (conexion.origen, conexion.linea))
            self.grafo.add_edge((conexion.origen, conexion.linea), (conexion.origen, None))

            self.grafo.add_edge((conexion.dest, None), (conexion.dest, conexion.linea))
            self.grafo.add_edge((conexion.dest, conexion.linea), (conexion.dest, None))

            self.grafo.add_edge((conexion.origen, conexion.linea), (conexion.dest, conexion.linea))
        
        for transbordo in transbordos:
            self.grafo.add_edge((transbordo.estacion, transbordo.linea1), (transbordo.estacion, transbordo.linea2))
            self.grafo.add_edge((transbordo.estacion, transbordo.linea2), (transbordo.estacion, transbordo.linea1))
