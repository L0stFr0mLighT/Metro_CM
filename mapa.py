from common.estacion import Estacion, Linea

from dataclasses import dataclass, field
from cairo import Context, ImageSurface, FORMAT_ARGB32
from PIL import Image
import math

def seleccionar_siguiente_estacion(linea_actual: Linea, estacion_actual: Estacion, visitados: set[str]) -> Estacion:
    vecinos = next(filter(lambda x: x[2] == linea_actual, estacion_actual.vecinos))

    v1, v2 = vecinos[0], vecinos[1]

    if v2 == None or v2.nombre in visitados:
        return v1
    else:
        return v2

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

    def set(self, estaciones: list[Estacion], lineas: list[Linea]):
        self.estaciones = estaciones
        self.lineas = lineas

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
                visitados.add(estacion_actual.nombre)

                x0, y0 = estacion_actual.pos_mapa[0], estacion_actual.pos_mapa[1]
                estacion_siguiente = seleccionar_siguiente_estacion(linea, estacion_actual, visitados) 
                # Dibujar recta
                especial = False
                if estacion_actual in recorrido and estacion_siguiente in recorrido:
                    if recorrido.index(estacion_actual) - recorrido.index(estacion_siguiente) in set([-1, 1]):
                        ctx.set_source_rgba(COLOR_REC[0], COLOR_REC[1], COLOR_REC[2])
                        especial = True
                if not especial:
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
    

