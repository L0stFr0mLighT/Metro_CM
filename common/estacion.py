from dataclasses import dataclass, field
from linea import Linea

@dataclass
class Estacion:
    nombre: str
    vecinos: list[tuple['Estacion', 'Estacion | None', Linea]] = field(default_factory=list)
    pos_mapa: tuple[float, float] = field(default_factory=tuple)
    # TODO: Añadir mas informacion si es necesario

    """ 
    Agrega dos vecinos a la estacion
    """
    def add_vecinos(self, v1: 'Estacion', v2: 'Estacion', linea: Linea):
        self.vecinos.append((v1, v2, linea))
    
    def add_unico_vecino(self, v: 'Estacion', linea: Linea):
        self.vecinos.append((v, None, linea))
