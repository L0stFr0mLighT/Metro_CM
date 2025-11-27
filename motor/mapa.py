from common.estacion import Estacion, Linea, Conexion, Transbordo

from motor import roundRect
from dataclasses import dataclass, field
from cairo import Context, ImageSurface, FORMAT_ARGB32
from PIL import Image
import math
import cairo

def to_pil(surface: ImageSurface) -> Image.Image:
    size = (surface.get_width(), surface.get_height())
    stride = surface.get_stride()

    with surface.get_data() as memory:
        return Image.frombuffer(
            "RGBA", size, memory.tobytes(),
            'raw', "BGRa", stride)

@dataclass
class Mapa:
    estaciones: dict[str, Estacion] = field(default_factory=dict)
    lineas: list[Linea] = field(default_factory=list)
    adyacentes: dict[tuple[Estacion, Linea], tuple[tuple[Estacion, float], tuple[Estacion, float] | None]] \
        = field(default_factory=dict)
    conexion: dict[tuple[Estacion, Estacion], tuple[Linea, float]] = field(default_factory=dict)
    transbordos: list[Transbordo] = field(default_factory=list)

    def set_mapa(self, estaciones: list[Estacion], lineas: list[Linea], conexiones: list[Conexion], transbordos: list[Transbordo]):
        # Formar la lista de transbordos
        self.transbordos = transbordos
        # Formar el diccionario de estaciones
        for estacion in estaciones:
            self.estaciones[estacion.nombre] = estacion
        self.lineas = lineas
        # Formar las adyacencias y conexiones
        for conexion in conexiones:
            self.conexion[(conexion.origen, conexion.dest)] = (conexion.linea, conexion.tiempo)

            elem = self.adyacentes.get((conexion.origen, conexion.linea))
            if elem == None:
                self.adyacentes[(conexion.origen, conexion.linea)] = ((conexion.dest, conexion.tiempo), None)
            else:
                self.adyacentes[(conexion.origen, conexion.linea)] = (elem[0], (conexion.dest, conexion.tiempo))

    def get_estaciones_adyacentes(self, est: Estacion, linea: Linea) -> tuple[Estacion, Estacion | None] | None:
        """
        Devuelve las estaciones adyacentes a la proporcionada, dada la linea.
        Si la estacion no esta en la linea, devuelve None
        """
        elem = self.adyacentes.get((est, linea))
        if elem == None:
            return None
        
        first = elem[0]
        second = elem[1]
        if second == None:
            return (first[0], None)
        return (first[0], second[0])

    def buscar_por_nombre(self, nombre: str) -> Estacion | None:
        """
        Devuelve la estacion con el nombre dado.
        None si dicha estacion no existe
        """
        return self.estaciones.get(nombre)

    def buscar_conexion(self, origen: Estacion, dest: Estacion) -> tuple[Linea, float] | None:
        return self.conexion.get((origen, dest))

    def buscar_transbordos(self, est: Estacion, l1: Linea, l2: Linea) -> Transbordo | None:
        """
        Devuelve la informacion de transbordo entre dos lineas en una estacion
        """
        for transbordo in self.transbordos:
            if transbordo.estacion == est:
                if transbordo.linea1 == l1 and transbordo.linea2 == l2:
                    return transbordo
                if transbordo.linea1 == l2 and transbordo.linea2 == l1:
                    return transbordo
        return None

    def seleccionar_siguiente_estacion(self, linea_actual: Linea, estacion_actual: Estacion, visitados: set[Estacion]) -> Estacion:
        vecinos = self.get_estaciones_adyacentes(estacion_actual, linea_actual)
        assert vecinos != None
        v1, v2 = vecinos[0], vecinos[1]

        if v2 == None or v2 in visitados:
            return v1
        return v2

    def dibujar_estaciones(self, res_x: int, res_y: int) -> Image.Image:
        return self.dibujar_estaciones_con_recorrido(res_x, res_y, [], step=0)[0]
    
    def dibujar_estaciones_con_recorrido(self, res_x: int, res_y: int, recorrido: list[Estacion], 
                                         step: float) -> tuple[Image.Image, bool]:
        
        FACTOR_ESCALA = 2
        COLOR_REC = (185.0 / 255, 122.0 / 255, 87.0 / 255)
        # TODO
        surface = ImageSurface(FORMAT_ARGB32, FACTOR_ESCALA * res_x, FACTOR_ESCALA * res_y)
        ctx = Context(surface)
        ctx.scale(float(FACTOR_ESCALA * res_x), float(FACTOR_ESCALA * res_y))

        for linea in self.lineas:
            visitados = set()
            estacion_actual = linea.cabeceras[0]
            
            lado = 0.05
            roundRect.roundrect(ctx, linea.pos_cuadrado[0], linea.pos_cuadrado[1], lado, lado, 0.01)
            ctx.close_path()
            ctx.set_source_rgba(linea.color[0], linea.color[1], linea.color[2])
            ctx.fill()
            ctx.set_line_width(0.002)
            roundRect.roundrect(ctx, linea.pos_cuadrado[0], linea.pos_cuadrado[1], lado, lado, 0.01)
            ctx.set_source_rgba(0, 0, 0)
            ctx.stroke()
            
            # Dibujar número centrado
            ctx.set_source_rgba(1, 1, 1)
            ctx.select_font_face("Arial", 0, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(0.03)
            te = ctx.text_extents(str(linea.numero))
            x_centro = linea.pos_cuadrado[0] + (lado - te.width) / 2 - te.x_bearing
            y_centro = linea.pos_cuadrado[1] + (lado - te.height) / 2 - te.y_bearing
            ctx.move_to(x_centro, y_centro)
            ctx.show_text(str(linea.numero))
            ctx.stroke()
            
            while estacion_actual != linea.cabeceras[1]:
                visitados.add(estacion_actual)

                x0, y0 = estacion_actual.pos_mapa[0], estacion_actual.pos_mapa[1]
                estacion_siguiente = self.seleccionar_siguiente_estacion(linea, estacion_actual, visitados) 
                # Dibujar recta
                ctx.set_source_rgba(linea.color[0], linea.color[1], linea.color[2])
                
                x1, y1 = estacion_siguiente.pos_mapa[0], estacion_siguiente.pos_mapa[1]
                ctx.set_line_width(0.01)
                ctx.move_to(x0, y0)
                ctx.line_to(x1, y1)
                ctx.stroke()

                estacion_actual = estacion_siguiente
                
                pass
            pass

        # Por cada estacion del recorrido, vamos dibujandolo
        for i in range(len(recorrido) - 1):
            if step == 0: break
            par_estaciones = recorrido[i:i+2]
            v1 = par_estaciones[0].pos_mapa
            v2 = par_estaciones[1].pos_mapa
            if i < step and step <= i + 1:
                # Calculamos vector director
                director = (v2[0] - v1[0], v2[1] - v1[1])
                director_pintado = ((step - i) * director[0], (step - i) * director[1])
                pos_final_pintado = (v1[0] + director_pintado[0], v1[1] + director_pintado[1])
                # Pintamos la parte proporcional
                ctx.set_line_width(0.01)
                ctx.set_source_rgba(COLOR_REC[0], COLOR_REC[1], COLOR_REC[2])
                ctx.move_to(v1[0], v1[1])
                ctx.line_to(pos_final_pintado[0], pos_final_pintado[1])
                ctx.stroke()
                break
            # El trozo actual debe estar completamente pintado
            ctx.set_line_width(0.01)
            ctx.set_source_rgba(COLOR_REC[0], COLOR_REC[1], COLOR_REC[2])
            ctx.move_to(v1[0], v1[1])
            ctx.line_to(v2[0], v2[1])
            ctx.stroke()

        for estacion in self.estaciones.values():
            ctx.set_line_width(0.005)
            ctx.arc(estacion.pos_mapa[0], estacion.pos_mapa[1], 0.005, 0.0, 2.0 * math.pi)
            ctx.close_path()
            ctx.set_source_rgba(1, 1, 1)
            ctx.fill()
            ctx.set_line_width(0.003)
            ctx.arc(estacion.pos_mapa[0], estacion.pos_mapa[1], 0.005, 0.0, 2.0 * math.pi)
            ctx.set_source_rgba(0, 0, 0)
            ctx.stroke()

            label = estacion.nombre        # Dibuja el nombre de la estación
            ctx.set_source_rgba(estacion.color[0]/255,estacion.color[1]/255, estacion.color[2]/255)   # Color
            ctx.set_font_size(0.02)        # Tamaño
            ctx.move_to(estacion.pos_nombre[0], estacion.pos_nombre[1]) # Posición
            ctx.show_text(label)

        surface.write_to_png("prueba.png")
        imagen = to_pil(surface)
        # Falta recorrido por pintar si step < len(recorrido) - 1
        return (imagen, step < (len(recorrido) - 1))
    
