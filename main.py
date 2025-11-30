import customtkinter
from estaciones import *
from motor.mapa import Mapa
from motor.grafo import Grafo
from PIL import Image, ImageTk
from tiempo.tiempo import sumar_hora, sumar_minutos
from CTkScrollableDropdown import CTkScrollableDropdown
from os import path
from ajustes import *
from ajustes import idioma
from idioma import *

# ----------------------------
mapa = Mapa()
mapa.set_mapa(ESTACIONES, LINEAS, CONEXIONES, TRANSBORDOS)

grafo = Grafo()
grafo.set_grafo(CONEXIONES, TRANSBORDOS, mapa)

RES_MAPA_X, RES_MAPA_Y = 700, 700

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
tiempo_total = ["00", "00"]
hora_estimada = ["00", "00"]
principales = list()

idioma = get_idioma()

# TODO
def buscar_rutas():
    """
    Llama al motor de rutas (A*), calcula el tiempo estimado del trayecto
    y lanza la animación del recorrido en el mapa.
    """
    global step, camino_animar, tiempo_inicio, id_linea, imagen_mapa_tk, estaciones_names, tiempo_total, hora_estimada

    origen_text = origen.get()
    destino_text = destino.get()
    menos_trasbordos = opcion1.get()
    baja_movilidad = opcion2.get() #TODO De momento no usado
    hora_salida = entry_hora.get()
    min_salida = entry_min.get()

    # Si falta origen o destino, no hacemos nada
    if origen_text not in estaciones_names or destino_text not in estaciones_names:
        mostrar_resultado([], hay_camino=False)
        return
    
    # Calcula el tiempo total del camino en minutos con A*
    camino = grafo.calcular_camino_minimo(origen_text, destino_text, bool(menos_trasbordos))
    if camino is None:
        mostrar_resultado([], hay_camino=False)
        return 

    # Calcula el tiempo total del camino en minutos
    minutos_camino = round(grafo.calcular_tiempo_camino(camino))
    tiempo_total = ["00", str(minutos_camino)]
    # Suma el tiempo de viaje a la hora de salida para obtener la hora estimada de llegada
    if int(hora_salida) >= 0 and int(hora_salida) < 5:
        diff_hora = 5-int(hora_salida)-1
        diff_min = diff_hora*60 + 60-int(min_salida)
        tiempo_total = sumar_minutos("00", str(minutos_camino), diff_min)
    hora_estimada = sumar_minutos(hora_salida, min_salida, minutos_camino)
    # camino: lista de (Estacion, Linea|None)  -> lo usamos para describir la ruta
    mostrar_resultado(camino,hay_camino=True)
    
    # Prepara el camino para la animación:
    # camino es una lista de tuplas (Estacion, Linea), nos quedamos solo con las Estaciones
    camino_dedup = list(dict.fromkeys(map(lambda x : x[0], camino)))
    
    # Limpia el canvas y vuelve a dibujar el mapa base de fondo
    imagen_mapa_tk = mapa.dibujar_estaciones(RES_MAPA_X, RES_MAPA_Y, customtkinter.get_appearance_mode() == "Dark")
    mapa_canvas.delete("all")
    mapa_canvas.create_image(0, 0, image=imagen_mapa_tk, anchor="nw")

    # Inicializa variables de animación
    tiempo_inicio = 0
    step = 0
    camino_animar = camino_dedup

    # Lanza la animación
    animar()

id_linea = 0
step = 0
camino_animar = list()
coordenadas = [(0, 0)]
DIRECTOR = (5, 5)

def animar():
    """
    Función recursiva (llamada periódicamente con after) que anima el recorrido
    del tren sobre el mapa, avanzando el parámetro 'step' poco a poco.
    """
    global mapaLabel, ventana, imagen_mapa_tk, tiempo_inicio, step, camino_animar, coordenadas
    PASO = 0.5      # Cuanto avanza el tren en cada frame
    PERIODO = 20    # Tiempo (ms) entre frames

    # Pinta el recorrido hasta el punto indicado por 'step'
    continuar = mapa.dibujar_estaciones_con_recorrido(RES_MAPA_X, RES_MAPA_Y, camino_animar, step, mapa_canvas)
    
    # Si todavía no ha llegado al final, incrementa step y reprograma la siguiente llamada
    if continuar:
        step = step + PASO
        mapa_canvas.after(PERIODO, animar)

def mostrar_resultado(camino_vertices: list[tuple[Estacion, Linea|None]], hay_camino: bool):
    global label1, labelResumenTitulo, labelDetalleTitulo, labelResumen, card, tiempo_total, hora_estimada, principales, idioma
    # ----- LIMPIAR CONTENIDO -----
    for widget in card.grid_slaves():
        if widget.grid_info().get("row", 0) != 0: # Mantener el título
            widget.grid_forget()

    # Caso sin ruta
    if not hay_camino or not camino_vertices:
        label1.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        return

    # ----- ORIGEN Y DESTINO -----
    principales = grafo.estaciones_principales(camino_vertices)

    idioma = get_idioma()
      
    # ====== (2) DETALLE  ======
    texto_detalle = get_texto_detalle(principales, idioma)
    labelTextoDetalle.configure(text=texto_detalle)
    labelTextoDetalle.grid(row=3, column=0, padx=25, pady=(0, 15), sticky="w")
    # ====== (1) RESUMEN ======
    resumen = get_resumen(principales, tiempo_total, hora_estimada, idioma)
    if(TRADUCCIONES[idioma]["detalles origen == destino"] != texto_detalle):
        labelDetalleTitulo.grid(row=2, column=0, padx=15, pady=(5, 5), sticky="w")
        labelResumenTitulo.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        labelResumen.configure(text=resumen)
        labelResumen.grid(row=1, column=0, padx=25, pady=(0, 15), sticky="w")



def character_limit_hour(entry_text):
    """
    Controla que el valor de la hora introducida sea válido (00–23).
    Se ejecuta cada vez que el usuario escribe en el campo de hora.
    """
    if len(entry_text.get()) > 0:
        primerCar = entry_text.get()[0]     # Coge el primer numero
        segundoCar = entry_text.get()[1:2]  # Coge el segundo numero
        if primerCar not in {"0", "1", "2"}: #Si no está en el rango de horas válidas, no saca nada
            entry_text.set("")
        elif primerCar == "2" and segundoCar not in {"0", "1", "2", "3"}:
            entry_text.set("2")
        elif segundoCar not in {"0", "1", "2", "3", "4", "5", "6","7","8","9"}:
            entry_text.set(primerCar)
        else:
            entry_text.set(entry_text.get()[:2])
   
def character_limit_min(entry_text):
    """
    Controla que el valor de minutos introducido sea válido (00–59).
    Se ejecuta cada vez que el usuario escribe en el campo de minutos.
    """
    if len(entry_text.get()) > 0:
        primerCar = entry_text.get()[0]
        segundoCar = entry_text.get()[1:2]
        if primerCar not in {"0", "1", "2", "3", "4", "5"}:
            entry_text.set("")
        elif segundoCar not in {"0", "1", "2", "3", "4", "5", "6","7","8","9"}:
            entry_text.set(primerCar)
        else:
            entry_text.set(entry_text.get()[:2])
            
def hora_button_callback(entry_hora, entry_min, paso):
    """
    Suma o resta 'paso' horas a la hora actual, respetando el formato HH
    y el ciclo de 24 horas.
    """
    (hora, min)= sumar_hora(entry_hora.get(), entry_min.get(), paso)
    entry_hora.set(hora)
    entry_min.set(min)

def min_button_callback(entry_hora, entry_min, paso):
    """
    Suma o resta 'paso' minutos a la hora actual, ajustando también la hora
    si hay desbordamiento por arriba o por abajo.
    """
    (hora, min)= sumar_minutos(entry_hora.get(), entry_min.get(), paso)
    entry_hora.set(hora)
    entry_min.set(min)
                
def cambio_ventana(tab):
    """
    Cambia entre las distintas vistas de la interfaz:
        - "programa": vista principal con formulario + mapa.
        - "about": vista 'Acerca de'.
        - "inicio": menú inicial.
    """
    match tab:
        case "programa":
            # Oculta la pantalla de inicio y muestra programa + mapa
            frame_inicio.grid_forget()
            ventana.grid_columnconfigure(1, weight=1)

            frameTexto.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
            frameMapa.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

            botonAjustesTitulo.grid(row=0, column=2, padx=10, pady=10, sticky="e") 
            botonVolverTitulo.grid(row=0, column=3, padx=10, pady=10, sticky="e")           
        case "about":
            # Oculta el inicio y muestra la ventana 'Acerca de'
            frame_inicio.grid_forget()
            frameTexto.grid_forget()
            frameMapa.grid_forget()
            botonAjustesTitulo.grid_forget()
            botonVolverTitulo.grid_forget()
            frameAbout.grid(row=1,column=0)
        case "inicio":
            # Vuelve al menú de inicio
            frameTexto.grid_forget()
            frameMapa.grid_forget()
            frameAbout.grid_forget()
            botonAjustesTitulo.grid_forget()
            botonVolverTitulo.grid_forget()
            ventana.grid_rowconfigure(1, weight=1)
            ventana.grid_columnconfigure(1, weight=0)
            frame_inicio.grid(row=1, column=0)

# ----------------------------
# Ventana principal y fuentes
# ----------------------------
ventana = customtkinter.CTk()

# Tamaño a pantalla completa (en píxeles)
ventana.geometry("{0}x{1}+0+0".format(ventana.winfo_screenwidth(), ventana.winfo_screenheight()))
ventana.iconbitmap(path.join(path.dirname(__file__), 'Imagenes/Logo_metro.ico'))
ventana.title("Metro Ciudad de Mexico")
ventana.minsize(1400,750)
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_rowconfigure(1, weight=1)

# Fuentes base de la interfaz
fuente_base = customtkinter.CTkFont(family="Roboto", size=16, weight="normal") # Fuente base para los textos
fuente_subtitulo = customtkinter.CTkFont(family= "Roboto", size=30, weight="normal")
fuente_titulo = customtkinter.CTkFont(family="Roboto", size= 40, weight="bold")

# Fuente específica para el texto de resultados (un poco más compacta)
fuente_resultado = customtkinter.CTkFont(family="Roboto", size=14, weight="normal")
fuente_resultado_titulo = customtkinter.CTkFont(family="Roboto", size=16, weight="bold")

# Lista de nombres de estaciones ordenada alfabéticamente para los combobox
estaciones_names = [e.nombre for e in ESTACIONES]
estaciones_names.sort()

# -----------------------------
# Frame inicio (menú principal)
# -----------------------------

# Frame con el menú de inicio (botón de iniciar, ajustes, acerca de, cerrar)
frame_inicio = customtkinter.CTkFrame(ventana, fg_color="transparent")
frame_inicio.grid(row=1, column=0, sticky="we")
frame_inicio.grid_columnconfigure(0, weight=1)

# Botón de "Inicio" con icono de play
play_image = customtkinter.CTkImage(light_image=Image.open(path.join(path.dirname(__file__), "Imagenes/play_light.png")).resize((50, 50)), 
                                        dark_image=Image.open(path.join(path.dirname(__file__), "Imagenes/play_dark.png")).resize((50, 50)), size=(50, 50)) # Botón inicio
boton_inicio = customtkinter.CTkButton(frame_inicio, image=play_image, text="Inicio", width=300, font=fuente_titulo, command= lambda : cambio_ventana("programa"))
boton_inicio.grid(row=0, column=0, padx=10, pady=(10,20))

ajustes_imagen = customtkinter.CTkImage(light_image=Image.open(path.join(path.dirname(__file__), "Imagenes/Ajustes_light.png")).resize((25, 25)), 
                                        dark_image=Image.open(path.join(path.dirname(__file__), "Imagenes/Ajustes_dark.png")).resize((25, 25)), size=(25, 25)) # Botón ajustes
botonAjustesInicio = customtkinter.CTkButton(frame_inicio, image=ajustes_imagen, text="Ajustes", width=300, font= fuente_base, 
                                             command= lambda : abrir_ajustes(ventana=ventana, fuentes=fuentesList, 
                                                                      labels=[etiqOrigen, etiqDestino, etiqSalida, etiqPreferencias, opcion1, opcion2, etiqResultado, boton_inicio, botonAjustesInicio, botonAbout, botonCerrarPrograma, label_acercaDe, label1, labelResumenTitulo, labelDetalleTitulo, labelTextoDetalle, labelResumen], canvas=mapa_canvas, 
                                                                      mapa=mapa, RES=[RES_MAPA_X, RES_MAPA_Y], 
                                                                      tiempo_total=tiempo_total, hora_estimada=hora_estimada, principales=principales))
botonAjustesInicio.grid(row=1, column=0, padx=10, pady=10)

about_imagen = customtkinter.CTkImage(light_image=Image.open(path.join(path.dirname(__file__), "Imagenes/About_light.png")).resize((25, 25)), 
                                        dark_image=Image.open(path.join(path.dirname(__file__), "Imagenes/About_dark.png")).resize((25, 25)), size=(25, 25))
botonAbout = customtkinter.CTkButton(frame_inicio, image=about_imagen, text="Acerca de", width=300, font=fuente_base, command=lambda : cambio_ventana("about"))
botonAbout.grid(row=2, column=0, padx=10, pady=10)

cerrar_imagen = customtkinter.CTkImage(light_image=Image.open(path.join(path.dirname(__file__), "Imagenes/Cerrar_light.png")).resize((25, 25)), 
                                        dark_image=Image.open(path.join(path.dirname(__file__), "Imagenes/Cerrar_dark.png")).resize((25, 25)), size=(25, 25))
botonCerrarPrograma = customtkinter.CTkButton(frame_inicio, image=cerrar_imagen, text="Cerrar", width=300, font=fuente_base, command=lambda : ventana.destroy())
botonCerrarPrograma.grid(row=3, column=0, padx=10, pady=10)

# ------------------
# Frame "Acerca de"
# ------------------
frameAbout = customtkinter.CTkFrame(ventana, fg_color="transparent")

botonVolverAbout = customtkinter.CTkButton(frameAbout, text= "Volver", font= fuente_base, command=lambda : cambio_ventana("inicio"))
botonVolverAbout.grid(row=1,column=0)

label_acercaDe = customtkinter.CTkLabel(frameAbout, font=fuente_base, text="Programa creado por:\n\nPablo Regidor Mendez\nDaniel Ramon Gragera\nYurong Cheng\nYun Chen\nAlvaro Vicente Bonilla\nJia Jie Ye")
label_acercaDe.grid(row=0, column=0, padx=10, pady=10, sticky="sw")

# -----------------------------
# Frame Titulo (barra superior)
# -----------------------------
frameTitulo = customtkinter.CTkFrame(ventana, fg_color=("white", "grey10"))
frameTitulo.grid(row=0, column=0, columnspan =2, sticky="ew", padx = 20, pady = 20)
frameTitulo.grid_columnconfigure(2, weight=1)

imagenLogo = customtkinter.CTkImage(light_image=Image.open(path.join(path.dirname(__file__), 'Imagenes/Logo_metro.ico')).resize((40,40)), size=(40,40))
labelLogo = customtkinter.CTkLabel(frameTitulo,image=imagenLogo, text="")
labelLogo.grid(row=0, column=0, padx = 20)
labelTitulo = customtkinter.CTkLabel(frameTitulo, text= "Metro Ciudad de México", font= fuente_titulo)
labelTitulo.grid(row=0,column=1)

# Botón ajustes en la barra superior (se muestra solo en modo "programa")
botonAjustesTitulo = customtkinter.CTkButton(frameTitulo, image=ajustes_imagen, text="", width=30, height=30, corner_radius=10, 
                                       command=lambda : abrir_ajustes(ventana=ventana, fuentes=fuentesList, 
                                                                      labels=[etiqOrigen, etiqDestino, etiqSalida, etiqPreferencias, opcion1, opcion2, etiqResultado, boton_inicio, botonAjustesInicio, botonAbout, botonCerrarPrograma, label_acercaDe, label1, labelResumenTitulo, labelDetalleTitulo, labelTextoDetalle, labelResumen], canvas=mapa_canvas, 
                                                                      mapa=mapa, RES=[RES_MAPA_X, RES_MAPA_Y], 
                                                                      tiempo_total=tiempo_total, hora_estimada=hora_estimada, principales=principales))

# Botón volver en la barra superior (se muestra solo en modo "programa")
volver_imagen = customtkinter.CTkImage(light_image=Image.open(path.join(path.dirname(__file__), "Imagenes/Volver_light.png")).resize((25, 25)), 
                                        dark_image=Image.open(path.join(path.dirname(__file__), "Imagenes/Volver_dark.png")).resize((25, 25)), size=(25, 25))
botonVolverTitulo = customtkinter.CTkButton(frameTitulo ,image=volver_imagen, text="", width=30, height=30, corner_radius=10, command=lambda: cambio_ventana("inicio"))

# -----------------------------------
# Frame izquierdo: formulario (texto)
# -----------------------------------
frameTexto = customtkinter.CTkFrame(ventana, fg_color=("grey80", "grey19")) # TODO:Color Provisional 
frameTexto.grid_columnconfigure((0,1), weight=1)
frameTexto.grid_rowconfigure(3, weight=1)
# frameTexto.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

# -------------------------
# Frame origen y destino
# -------------------------
frameOrigen_Destino = customtkinter.CTkFrame(frameTexto, fg_color= "transparent", corner_radius=6)
frameOrigen_Destino.grid_columnconfigure((0,1), weight=1)
frameOrigen_Destino.grid(row=0, column=0, sticky="nsew", columnspan= 2, pady=10, padx=1)

etiqOrigen = customtkinter.CTkLabel(frameOrigen_Destino, text="Origen", font=fuente_base, corner_radius=6)
etiqOrigen.grid(row=0, column=0, padx=(0,18), sticky="ew")
etiqDestino = customtkinter.CTkLabel(frameOrigen_Destino, text="Destino", font=fuente_base, corner_radius=6)
etiqDestino.grid(row=0, column=1, padx=(0,18), sticky="ew")  


origen = customtkinter.CTkComboBox(frameOrigen_Destino, font=fuente_base, justify="center", width=225)
CTkScrollableDropdown(origen, values=estaciones_names, autocomplete=True, scrollbar=False, double_click=False)
origen.grid(row=1, column=0)

destino = customtkinter.CTkComboBox(frameOrigen_Destino, font=fuente_base, justify="center", width=225)
CTkScrollableDropdown(destino, values=estaciones_names, autocomplete=True, scrollbar=False, double_click=False)
destino.grid(row=1, column=1)

lupa_imagen = customtkinter.CTkImage(light_image=Image.open(path.join(path.dirname(__file__), "Imagenes/lupa_light.png")).resize((25, 25)),
                                     dark_image=Image.open(path.join(path.dirname(__file__), "Imagenes/lupa_dark.png")).resize((25, 25)), size=(25, 25)) # Botón lupa
botonBuscar = customtkinter.CTkButton(frameOrigen_Destino, command=buscar_rutas, image=lupa_imagen, text="", width=50, height=50, corner_radius=10)
botonBuscar.grid(row=0, column=2, rowspan=2, padx=10)

# -------------------
# Frame entrada hora
# -------------------
frameEntryTiempo = customtkinter.CTkFrame(frameTexto, fg_color= "transparent")
frameEntryTiempo.grid_columnconfigure((0,2), weight=1)
frameEntryTiempo.grid(row=1, column=0, sticky="wns", pady=10, padx=1)

entry_hora = customtkinter.StringVar(ventana, "00") # Etiqueta y Entrys para la hora de salida
entry_min = customtkinter.StringVar(ventana, "00")

etiqSalida = customtkinter.CTkLabel(frameEntryTiempo, text="Hora de salida (HH:MM):", font=fuente_base)
etiqSalida.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0,5), padx=(20,0))


masHora = customtkinter.CTkButton(frameEntryTiempo, text="+", width=50, height=20, font=fuente_base, command=lambda: hora_button_callback(entry_hora, entry_min, 1))
masHora.grid(row=1, column=0, sticky="e", padx=5)
menosHora = customtkinter.CTkButton(frameEntryTiempo, text="-", width=50, height=20, font=fuente_base, command=lambda: hora_button_callback(entry_hora, entry_min, -1))
menosHora.grid(row=3, column=0, sticky="e", padx=5)

masMin = customtkinter.CTkButton(frameEntryTiempo, text="+", width=50, height=20, font=fuente_base, command=lambda: min_button_callback(entry_hora, entry_min, 5))
masMin.grid(row=1, column=2, sticky="w", padx=5)
menosMin = customtkinter.CTkButton(frameEntryTiempo, text="-", width=50, height=20, font=fuente_base, command=lambda: min_button_callback(entry_hora, entry_min, -5))
menosMin.grid(row=3, column=2, sticky="w", padx=5)


hora = customtkinter.CTkEntry(frameEntryTiempo, width=50, height=20,textvariable=entry_hora, font=fuente_base)
hora.grid(row=2, column=0, sticky="e", padx=5)
entry_hora.trace("w", lambda *args: character_limit_hour(entry_hora))
dosPuntos = customtkinter.CTkLabel(frameEntryTiempo, text=":", font=fuente_base)
dosPuntos.grid(row=2, column=1, sticky="ew")
minuto = customtkinter.CTkEntry(frameEntryTiempo,width=50, height=20, textvariable=entry_min, font=fuente_base)
minuto.grid(row=2, column=2, sticky="w", padx=5)
entry_min.trace("w", lambda *args: character_limit_min(entry_min))

# --------------------
# Frame Preferencias
# --------------------
framePreferencias = customtkinter.CTkFrame(frameTexto, fg_color="transparent")
framePreferencias.grid_columnconfigure(0, weight=1)
framePreferencias.grid(row=1, column=1, sticky="nsew", pady=10, padx=1)

etiqPreferencias = customtkinter.CTkLabel(framePreferencias, text="Preferencias de viaje:", font=fuente_base)
etiqPreferencias.grid(row=0, column=0, pady=(0,5), sticky="w")
opcion1 = customtkinter.CTkCheckBox(framePreferencias, text="Menos trasbordos", font=fuente_base,)
opcion1.grid(row=1, column=0, pady=(10,5), sticky="w")
opcion2 = customtkinter.CTkCheckBox(framePreferencias, text="Baja Movilidad", font=fuente_base)
opcion2.grid(row=2, column=0, pady=5, sticky="w")

#TODO: Imprimir imprimir busqueda en el frame resultado
# ----------------
# Frame resultado
# ----------------
frameResultado = customtkinter.CTkFrame(frameTexto, border_width=2, fg_color="transparent", border_color=("black", "white"))
frameResultado.grid_columnconfigure(0, weight=1)
frameResultado.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10, padx=10)
frameResultado.grid_rowconfigure(1, weight=1)

etiqResultado = customtkinter.CTkLabel(frameResultado, text="Ruta óptima", font=fuente_subtitulo)
etiqResultado.grid(row=0, column=0, pady = (20,0))

    # ----- TARJETA -----
card = customtkinter.CTkFrame(frameResultado, fg_color=("gray90", "gray20"), corner_radius=10)
card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
card.grid_columnconfigure(0, weight=1)
label1 = customtkinter.CTkLabel(card, text="No existe ruta entre las estaciones seleccionadas.", font=fuente_base, anchor="w")
labelResumenTitulo = customtkinter.CTkLabel(card, text="Resumen del trayecto", font=fuente_resultado_titulo, anchor="w")
labelResumen = customtkinter.CTkLabel(card, text="1", font=fuente_resultado, anchor="w", justify="left")
labelDetalleTitulo = customtkinter.CTkLabel(card, text="Detalle del recorrido", font=fuente_resultado_titulo, anchor="w")
labelTextoDetalle = customtkinter.CTkLabel(card, text="2", font=fuente_resultado, anchor="w", justify="left", wraplength=600)
# -----------------------------
# Frame principal derecho (mapa)
# -----------------------------
frameMapa = customtkinter.CTkFrame(ventana, fg_color="transparent")
frameMapa.grid_columnconfigure(0, weight=1)
frameMapa.grid_rowconfigure(0, weight=1)
# frameMapa.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

color_canvas = "grey14" if customtkinter.get_appearance_mode() == "Dark" else "grey92"

imagen_mapa_tk = mapa.dibujar_estaciones(RES_MAPA_X, RES_MAPA_Y, customtkinter.get_appearance_mode() == "Dark")
mapa_canvas = customtkinter.CTkCanvas(frameMapa, height=imagen_mapa_tk.height(), width=imagen_mapa_tk.width(), highlightthickness=0, background=color_canvas)
mapa_canvas.create_image(0, 0, image=imagen_mapa_tk, anchor="nw")
mapa_canvas.grid(row=0, column=0, sticky="nsew")

# labelsList=[etiqOrigen, etiqDestino, etiqSalida, etiqPreferencias, opcion1, opcion2, etiqResultado, boton_inicio, botonAjustesInicio, botonAbout, botonCerrarPrograma, label_acercaDe, label1, labelResumenTitulo, labelDetalleTitulo, labelTextoDetalle, labelResumen]
fuentesList=[fuente_base, fuente_subtitulo, fuente_titulo, fuente_resultado, fuente_resultado_titulo]

ventana.mainloop()