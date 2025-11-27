from dataclasses import dataclass, field

@dataclass(eq=True, frozen=True)
class Estacion:
    """
    Representa una estacion
    """
    nombre: str
    pos_mapa: tuple[float, float]
    coordenadas: tuple[float, float]
    pos_nombre: tuple[float, float]
    color: tuple[float, float, float] = (0.0, 0.0, 0.0)
    # TODO: Añadir mas informacion si es necesario

@dataclass(eq=True, frozen=True)
class Linea:
    """
    Representa una linea
    """
    numero: int
    cabeceras: tuple[Estacion, Estacion]
    color: tuple[float, float, float]

    @classmethod
    def crear_linea(cls, numero: int,cabeceras: tuple[Estacion, Estacion], color: tuple[float, float, float]) -> 'Linea':
        return Linea(numero, cabeceras, (color[0] / 255, color[1] / 255, color[2] / 255))

@dataclass
class Conexion:
    """
    Representa una conexion de dos estaciones a traves de una linea
    NOTA: No se puede tratar como un tipo simetrico; es decir, 
    {est1, est2, linea, tiempo} != {est2, est1, linea, tiempo}
    """
    origen: Estacion
    dest: Estacion
    linea: Linea
    tiempo: float

    def simetrico(self) -> 'Conexion':
        return Conexion(self.dest, self.origen, self.linea, self.tiempo)

@dataclass
class Transbordo:
    """
    Representa un trasbordo de dos lineas en una estacion. Se verifica
    {est, linea1, linea2, t} == {est, linea2, linea1, t}
    """
    estacion: Estacion
    linea1: Linea
    linea2: Linea
    tiempo_trasbordo: float    
