from estaciones import ESTACIONES
from common.estacion import Estacion, Linea

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

def seleccionar_siguiente_estacion(linea_actual: Linea, estacion_actual: Estacion, visitados: set[str]) -> Estacion:
    vecinos = next(filter(lambda x: x[2] == linea_actual, estacion_actual.vecinos))

    v1, v2 = vecinos[0], vecinos[1]

    if v2 == None or v2.nombre in visitados:
        return v1
    else:
        return v2

def dibujar_estaciones(estaciones: list[Estacion], lineas: list[Linea], res_x: int, res_y: int):
    # TODO
    surface = ImageSurface(FORMAT_ARGB32, 3 * res_x, 3 * res_y)
    ctx = Context(surface)
    ctx.scale(float(3 * res_x), float(3 * res_y))

    for linea in lineas:
        visitados = set()
        estacion_actual = linea.cabeceras[0]
        while estacion_actual != linea.cabeceras[1]:
            visitados.add(estacion_actual.nombre)
            # Dibujar estacion
            x0, y0 = estacion_actual.pos_mapa[0], estacion_actual.pos_mapa[1]
            ctx.set_source_rgba(0, 0, 0)
            ctx.set_line_width(0.005)
            ctx.arc(x0, y0, 0.005, 0, 2 * math.pi)
            ctx.stroke()

            estacion_siguiente = seleccionar_siguiente_estacion(linea, estacion_actual, visitados) 
            # Dibujar recta
            x1, y1 = estacion_siguiente.pos_mapa[0], estacion_siguiente.pos_mapa[1]
            ctx.set_source_rgba(linea.color[0], linea.color[1], linea.color[2])
            ctx.set_line_width(0.05)
            ctx.move_to(x0, y0)
            ctx.line_to(x1, y1)
            ctx.stroke()

            estacion_actual = estacion_siguiente
            
            pass
        pass

    surface.write_to_png("prueba.png")
    # imagen = to_pil(surface)
    # TODO
    pass
