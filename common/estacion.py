from dataclasses import dataclass, field

@dataclass
class Linea:
    numero: int
    cabeceras: tuple['Estacion', 'Estacion'] = field(default_factory=tuple)
    color: tuple[float, float, float] = field(default_factory=tuple)

    def set_cabeceras(self, cabeceras: tuple['Estacion', 'Estacion']):
        self.cabeceras = cabeceras
    
    def set_color(self, red: float, green: float, blue: float):
        self.color = (red / 255, green / 255, blue / 255)


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
    
    """
    Agrega un unico vecino
    """
    def add_unico_vecino(self, v: 'Estacion', linea: Linea):
        self.vecinos.append((v, None, linea))
    
    def set_pos_mapa(self, pos: tuple[float, float]):
        self.pos_mapa = pos
