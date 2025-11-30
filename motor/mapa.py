from common.estacion import Estacion, Linea, Conexion, Transbordo

from motor import roundRect
from dataclasses import dataclass, field
from cairo import Context, ImageSurface, FORMAT_ARGB32
from PIL import Image
import math
import cairo
from customtkinter import CTkCanvas

FACTOR_ESCALA = 1.25

#Dibujo de Cairo a PIL
def to_pil(surface: ImageSurface) -> Image.Image:
    size = (surface.get_width(), surface.get_height())
    stride = surface.get_stride()

    with surface.get_data() as memory:
        return Image.frombuffer(
            "RGBA", size, memory.tobytes(),
            'raw', "BGRa", stride)

@dataclass
class Mapa:
    """
    Representa el mapa de la red de Metro
    Se debe inicializar con Mapa.set_mapa
    """
    # Nombre_Estacion -> Estacion
    estaciones: dict[str, Estacion] = field(default_factory=dict)
    lineas: list[Linea] = field(default_factory=list)
    # (Estacion, Linea) -> ((Estacion, tiempo), (Estacion, tiempo) | None) 
    # Si es cabecera, el segundo elemento es None
    adyacentes: dict[tuple[Estacion, Linea], tuple[tuple[Estacion, float], tuple[Estacion, float] | None]] \
        = field(default_factory=dict)
    # (Estacion_origen, Estacion_dest) -> (Linea, tiempo)
    conexion: dict[tuple[Estacion, Estacion], tuple[Linea, float]] = field(default_factory=dict)
    transbordos: list[Transbordo] = field(default_factory=list)
    
    _mapa_actual: ImageSurface | None = field(default_factory=lambda : None)
    _ctx: Context | None = field(default_factory=lambda : None)
    _id_curva_recorrido: int | None = field(default_factory=lambda : None)
    _curva_recorrido: list[tuple[int, int]] = field(default_factory=list)
    _primer_render: bool = field(default_factory=lambda : False)

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

            #Dado una conexion entre dos estaciones, miramos si desde la estacion origen ya hay vecinos
            elem = self.adyacentes.get((conexion.origen, conexion.linea))
            if elem == None: # Si no hay vecinos, lo añadimos directamente
                self.adyacentes[(conexion.origen, conexion.linea)] = ((conexion.dest, conexion.tiempo), None)
            else: # Si ya hay vecinos, añadimos el nuevo en la segunda posicion (significa que ya hemos visitado la estacion antes)
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
        if second == None: # Es cabecera
            return (first[0], None)
        return (first[0], second[0])

    def buscar_por_nombre(self, nombre: str) -> Estacion | None:
        """
        Devuelve la estacion con el nombre dado.
        None si dicha estacion no existe
        """
        return self.estaciones.get(nombre)

    def buscar_conexion(self, origen: Estacion, dest: Estacion) -> tuple[Linea, float] | None:
        """
        Devuelve la linea de conexion entre dos estaciones y el tiempo de viaje.
        None si no existe dicha conexion
        """
        return self.conexion.get((origen, dest))

    def buscar_transbordos(self, est: Estacion, l1: Linea, l2: Linea) -> Transbordo | None:
        """
        Devuelve la informacion de transbordo entre dos lineas en una estacion.
        None si no existe dicho transbordo
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
        """
        Dada una linea y una estacion, selecciona la siguiente estacion a visitar
        """
        assert vecinos != None
        v1, v2 = vecinos[0], vecinos[1]

        if v2 == None or v2 in visitados:
            return v1
        return v2

    def _dibujar_mapa_inicial(self, res_x: int, res_y: int):
        """
        Pinta el mapa inicial, inicializando la superficie de imagen
        """
        # Creo imgagen en blanco donde dibujar
        self._mapa_actual = ImageSurface(FORMAT_ARGB32, int(FACTOR_ESCALA * res_x), int(FACTOR_ESCALA * res_y))
        # Creo contexto de dibujo: le explico que voy a dibujar en la imagen creada
        self._ctx = Context(self._mapa_actual)
        # Escalo el contexto para que se adapte a la resolucion dada
        self._ctx.scale(float(FACTOR_ESCALA * res_x), float(FACTOR_ESCALA * res_y))

        for linea in self.lineas:
            visitados = set()
            estacion_actual = linea.cabeceras[0]
            
            # Dibujar cuadro para el número de línea
            lado = 0.05
            roundRect.roundrect(self._ctx, linea.pos_cuadrado[0], linea.pos_cuadrado[1], lado, lado, 0.01)
            self._ctx.close_path()
            self._ctx.set_source_rgba(linea.color[0], linea.color[1], linea.color[2])
            self._ctx.fill()
            # Dibujo el borde negro para el cuadrado del número de línea
            self._ctx.set_line_width(0.002)
            roundRect.roundrect(self._ctx, linea.pos_cuadrado[0], linea.pos_cuadrado[1], lado, lado, 0.01)
            self._ctx.set_source_rgba(0, 0, 0)
            self._ctx.stroke()
            
            # Dibujar número centrado dentro del cuadrado
            self._ctx.set_source_rgba(1, 1, 1) #Color blanco
            self._ctx.select_font_face("Arial", 0, cairo.FONT_WEIGHT_BOLD)
            self._ctx.set_font_size(0.03)
            te = self._ctx.text_extents(str(linea.numero)) #Pregunta a Cairo cuánto ocupa el texto
            x_centro = linea.pos_cuadrado[0] + (lado - te.width) / 2 - te.x_bearing # Consigo la posición centrada
            y_centro = linea.pos_cuadrado[1] + (lado - te.height) / 2 - te.y_bearing
            self._ctx.move_to(x_centro, y_centro) 
            self._ctx.show_text(str(linea.numero)) #Dibujo el número de línea
            self._ctx.stroke()
            
            #Segmentos entre estaciones de una línea
            while estacion_actual != linea.cabeceras[1]:
                visitados.add(estacion_actual)

                x0, y0 = estacion_actual.pos_mapa[0], estacion_actual.pos_mapa[1]
                estacion_siguiente = self.seleccionar_siguiente_estacion(linea, estacion_actual, visitados) 
                # Dibujar recta
                self._ctx.set_source_rgba(linea.color[0], linea.color[1], linea.color[2])
                x1, y1 = estacion_siguiente.pos_mapa[0], estacion_siguiente.pos_mapa[1]
                self._ctx.set_line_width(0.01)
                self._ctx.move_to(x0, y0) # Punto inicial
                self._ctx.line_to(x1, y1) # Punto final
                self._ctx.stroke()

                estacion_actual = estacion_siguiente
                
                pass
            pass
        # Dibujo las estaciones encima de las líneas
        for estacion in self.estaciones.values():
            
            #Dibuja el punto de la estación
            self._ctx.set_line_width(0.005)
            self._ctx.arc(estacion.pos_mapa[0], estacion.pos_mapa[1], 0.005, 0.0, 2.0 * math.pi)
            self._ctx.close_path()
            self._ctx.set_source_rgba(1, 1, 1)
            self._ctx.fill()

            #Dibuja el borde del punto de la estación
            self._ctx.set_line_width(0.003)
            self._ctx.arc(estacion.pos_mapa[0], estacion.pos_mapa[1], 0.005, 0.0, 2.0 * math.pi)
            self._ctx.set_source_rgba(0, 0, 0)
            self._ctx.stroke()

            # Dibuja el nombre de la estación
            label = estacion.nombre
            self._ctx.set_source_rgba(estacion.color[0]/255,estacion.color[1]/255, estacion.color[2]/255)   # Color
            self._ctx.set_font_size(0.02)        # Tamaño
            self._ctx.move_to(estacion.pos_nombre[0], estacion.pos_nombre[1]) # Posición
            self._ctx.show_text(label)      # Dibuja el texto

    def dibujar_estaciones(self, res_x: int, res_y: int) -> Image.Image:
        """
        Dibuja el mapa desde cero
        """
        self._mapa_actual = None
        self._ctx = None
        self._id_curva_recorrido = None
        self._curva_recorrido = list()
        self._dibujar_mapa_inicial(res_x, res_y)
        assert self._mapa_actual != None
        return to_pil(self._mapa_actual)
    
    def dibujar_estaciones_con_recorrido(self, res_x: int, res_y: int, recorrido: list[Estacion], 
                                         step: float, canvas: CTkCanvas | None) -> bool:
        """
        Dibuja el mapa con el recorrido en el canvas dado con el paso dado. 
        Si no se ha dibujado el mapa previamente, lo crea
        Si tienes que continuar, devuelve True
        """
        COLOR_REC = "red"
        if self._mapa_actual == None:
            self._dibujar_mapa_inicial(res_x, res_y)

        assert self._mapa_actual != None

        if canvas == None:
            self._mapa_actual.write_to_png("prueba.png")
            return False
        
        # Por cada estacion del recorrido, vamos dibujandolo
        for i in range(len(recorrido) - 1):
            par_estaciones = recorrido[i:i+2]
            v1 = par_estaciones[0].pos_mapa
            v2 = par_estaciones[1].pos_mapa
            
            if step == 0: 
                self._curva_recorrido = [escalar(res_x, res_y, v1[0], v1[1])]
                self._primer_render = True
                break

            if i < step and step <= i + 1:
                # Calculamos vector director
                director = (v2[0] - v1[0], v2[1] - v1[1])
                director_pintado = ((step - i) * director[0], (step - i) * director[1])
                pos_final_pintado = (v1[0] + director_pintado[0], v1[1] + director_pintado[1])
                # Pintamos la parte proporcional
                self._curva_recorrido.append(escalar(res_x, res_y, pos_final_pintado[0], pos_final_pintado[1]))

            if step > len(recorrido) - 1:
                # El paso es demasiado grande, pintamos hasta el final
                self._curva_recorrido.append(escalar(res_x, res_y, recorrido[-1].pos_mapa[0], recorrido[-1].pos_mapa[1]))

            if self._primer_render:
                self._id_curva_recorrido = canvas.create_line(*self._curva_recorrido, 
                                                              width=0.01 * FACTOR_ESCALA * res_x,
                                                              fill=COLOR_REC)
                self._primer_render = False
            else:
                canvas.coords(self._id_curva_recorrido, *self._curva_recorrido)

            # Dibujar los puntos de las estaciones
            crear_circulo(*escalar(res_x, res_y, v1[0], v1[1]), int(0.005 * FACTOR_ESCALA * res_x), 
                          canvas, fill="black")
            crear_circulo(*escalar(res_x, res_y, v1[0], v1[1]), int(0.004 * FACTOR_ESCALA * res_x),
                          canvas, fill="white")

            if i < step and step <= i + 1:
                break
            pass # for i in range(len(recorrido) - 1)
        # Si estamos en el paso final, dibujamos el punto del tren encima de la estacion
        if len(recorrido) > 0 and step >= len(recorrido) - 1:
            crear_circulo(*escalar(res_x, res_y, recorrido[-1].pos_mapa[0], recorrido[-1].pos_mapa[1]), 
                          int(0.005 * FACTOR_ESCALA * res_x), canvas, fill="green")
        
        # Falta recorrido por pintar si step < len(recorrido) - 1
        return step < (len(recorrido) - 1)
    
def crear_circulo(x: int, y: int, r: int, canvas: CTkCanvas, **kwargs):
    """
    Crea un circulo en el canvas dado.
    """
    return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def escalar(res_x: int, res_y: int, x: float, y: float) -> tuple[int, int]:
    """
    Aplica una transformacion de escala al vector (x, y) por la resolucion dada.
    Emula a Pycairo
    """
    escalar_x, escalar_y = float(FACTOR_ESCALA * res_x), float(FACTOR_ESCALA * res_y)
    return (int(x * escalar_x), int(y * escalar_y))
