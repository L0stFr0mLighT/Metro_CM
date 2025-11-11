from dataclasses import dataclass, field
from linea import Linea

@dataclass
class Estacion:
    nombre: str
    vecinos: list[tuple['Estacion', 'Estacion', Linea]] = field(default_factory=list)
    pos_mapa: tuple[float, float] = field(default_factory=tuple)
    # TODO: Añadir mas informacion si es necesario
