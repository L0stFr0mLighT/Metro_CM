from networkx import Graph

from common.estacion import Estacion

class Grafo:
    def Grafo(self, estaciones: list[Estacion]):
        # TODO: Añadir mas datos aqui
        self.grafo = Graph()
        for estacion in estaciones:
            for vecino in estacion.vecinos:
                # TODO: Añadir los costes de los viajes
                if vecino[0] != None:
                    self.grafo.add_edge(vecino[0], estacion)
                if vecino[1] != None:
                    self.grafo.add_edge(vecino[1], estacion)
                    
        