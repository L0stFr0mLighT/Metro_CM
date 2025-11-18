from common.estacion import Estacion, Linea, Conexion

from dataclasses import dataclass, field
from cairo import Context, ImageSurface, FORMAT_ARGB32
from PIL import Image
import math

def to_pil(surface: ImageSurface) -> Image.Image:
    size = (surface.get_width(), surface.get_height())
    stride = surface.get_stride()

    with surface.get_data() as memory:
        return Image.frombuffer(
            "RGBA", size, memory.tobytes(),
            'raw', "BGRa", stride)

@dataclass
class Mapa:
    estaciones: list[Estacion] = field(default_factory=list)
    lineas: list[Linea] = field(default_factory=list)
    conexion: dict[tuple[Estacion, Linea], tuple[tuple[Estacion, float], tuple[Estacion, float] | None]] \
        = field(default_factory=dict)

    def set_mapa(self, estaciones: list[Estacion], lineas: list[Linea], conexiones: list[Conexion]):
        self.estaciones = estaciones
        self.lineas = lineas
        for conexion in conexiones:
            elem = self.conexion.get((conexion.origen, conexion.linea))
            if elem == None:
                self.conexion[(conexion.origen, conexion.linea)] = ((conexion.dest, conexion.tiempo), None)
            else:
                self.conexion[(conexion.origen, conexion.linea)] = (elem[0], (conexion.dest, conexion.tiempo))

    """
    Devuelve las estaciones adyacentes a la proporcionada, dada la linea.
    Si la estacion no esta en la linea, devuelve None
    """
    def get_estaciones_adyacentes(self, est: Estacion, linea: Linea) -> tuple[Estacion, Estacion | None] | None:
        elem = self.conexion.get((est, linea))
        if elem == None:
            return None
        
        first = elem[0]
        second = elem[1]
        if second == None:
            return (first[0], None)
        return (first[0], second[0])

    def seleccionar_siguiente_estacion(self, linea_actual: Linea, estacion_actual: Estacion, visitados: set[Estacion]) -> Estacion:
        vecinos = self.get_estaciones_adyacentes(estacion_actual, linea_actual)
        assert vecinos != None
        v1, v2 = vecinos[0], vecinos[1]

        if v2 == None or v2 in visitados:
            return v1
        return v2

    def dibujar_estaciones(self, res_x: int, res_y: int) -> Image.Image:
        return self.dibujar_estaciones_con_recorrido(res_x, res_y, [])
    
    def dibujar_estaciones_con_recorrido(self, res_x: int, res_y: int, recorrido: list[Estacion]) -> Image.Image:
        FACTOR = 2
        COLOR_REC = (185.0 / 255, 122.0 / 255, 87.0 / 255)
        # TODO
        surface = ImageSurface(FORMAT_ARGB32, FACTOR * res_x, FACTOR * res_y)
        ctx = Context(surface)
        ctx.scale(float(FACTOR * res_x), float(FACTOR * res_y))

        for linea in self.lineas:
            visitados = set()
            estacion_actual = linea.cabeceras[0]
            while estacion_actual != linea.cabeceras[1]:
                visitados.add(estacion_actual)

                x0, y0 = estacion_actual.pos_mapa[0], estacion_actual.pos_mapa[1]
                estacion_siguiente = self.seleccionar_siguiente_estacion(linea, estacion_actual, visitados) 
                # Dibujar recta
                enRecorrido = False
                if estacion_actual in recorrido and estacion_siguiente in recorrido:
                    if recorrido.index(estacion_actual) - recorrido.index(estacion_siguiente) in set([-1, 1]):
                        ctx.set_source_rgba(COLOR_REC[0], COLOR_REC[1], COLOR_REC[2])
                        enRecorrido = True
                if not enRecorrido:
                    ctx.set_source_rgba(linea.color[0], linea.color[1], linea.color[2])
                
                x1, y1 = estacion_siguiente.pos_mapa[0], estacion_siguiente.pos_mapa[1]
                ctx.set_line_width(0.01)
                ctx.move_to(x0, y0)
                ctx.line_to(x1, y1)
                ctx.stroke()

                estacion_actual = estacion_siguiente
                
                pass
            pass

        for estacion in self.estaciones: 
                ctx.set_line_width(0.005)
                ctx.arc(estacion.pos_mapa[0], estacion.pos_mapa[1], 0.005, 0.0, 2.0 * math.pi)
                ctx.close_path()
                ctx.set_source_rgba(1, 1, 1)
                ctx.fill()
                ctx.set_line_width(0.003)
                ctx.arc(estacion.pos_mapa[0], estacion.pos_mapa[1], 0.005, 0.0, 2.0 * math.pi)
                ctx.set_source_rgba(0, 0, 0)
                ctx.stroke()

        surface.write_to_png("prueba.png")
        imagen = to_pil(surface)
        return imagen
    
