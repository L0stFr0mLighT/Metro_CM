import customtkinter
from motor.mapa import Mapa
from PIL import ImageTk
from common.estacion import Estacion


# Diccionario con todos los textos de la interfaz según el idioma seleccionado.
# Cada clave principal es un idioma, y dentro hay las traducciones de cada etiqueta.
TRADUCCIONES = {
    "Español": {
        "idiomas": ["Español", "Inglés", "Francés"],
        "titulo_ajustes": "Ajustes",
        "apariencia": "Apariencia",
        "etiq_origen": "Origen",
        "etiq_destino": "Destino",
        "etiq_Salida": "Hora de salida (HH:MM):",
        "etiq_Preferencias": "Preferencias de viaje:",
        "opcion1": "Menos trasbordos",
        "opcion2": "Baja Movilidad",
        "resultado": "Ruta óptima",
        "inicio": "Inicio",
        "ajustes": "Ajustes",
        "acercaDe": "Acerca de",
        "cerrar": "Cerrar",
        "formatoLetra": "Formato de letra:",
        "idioma": "Idioma:"
    },
    "Inglés": {
        "idiomas": ["Spanish", "English", "French"],
        "titulo_ajustes": "Settings",
        "apariencia": "Appearance",
        "etiq_origen": "Beginning",
        "etiq_destino": "Destination",
        "etiq_Salida": "Departure time (HH:MM):",
        "etiq_Preferencias": "Travel preferences:",
        "opcion1": "Fewer transfers",
        "opcion2": "Low mobility",
        "resultado": "Optimal route",
        "inicio": "Start",
        "ajustes": "Settings",
        "acercaDe": "About",
        "cerrar": "Close",
        "formatoLetra": "Font format:",
        "idioma": "Language:",
    },
    "Francés": {
        "idiomas": ["Espagnol", "Anglais", "Français"],
        "titulo_ajustes": "Paramètres",
        "apariencia": "Apparence",
        "etiq_origen": "Origine",
        "etiq_destino": "Destination",
        "etiq_Salida": "Heure de départ (HH:MM):",
        "etiq_Preferencias": "Préférences de voyage:",
        "opcion1": "Moins de transferts",
        "opcion2": "Mobilité réduite",
        "resultado": "Itinéraire optimale",
        "inicio": "Commencer",
        "ajustes": "Ajustements",
        "acercaDe": "À propos de",
        "cerrar": "Fermer",
        "formatoLetra": "Police format:",
        "idioma": "Langue:",
    }
}

IDIOMAS = ["Español", "Inglés", "Francés"]
idioma = "Español"

def abrir_ajustes(ventana: customtkinter.CTk, fuentes : list[customtkinter.CTkFont], labels : list[customtkinter.CTkLabel],
                  canvas: customtkinter.CTkCanvas, mapa: Mapa, camino_anim: list[Estacion], RES: tuple[int, int]):
    """
    Crea y muestra una ventana de ajustes sobre la ventana principal,
    desde la que se puede cambiar tema, idioma y tipografía.
    """
     # Ventana modal de ajustes
    ajustes = customtkinter.CTkToplevel(ventana)
    ajustes.title(TRADUCCIONES[idioma]["titulo_ajustes"])
    ajustes.focus_force()                             # Trae la ventana de ajustes al frente
    ajustes.grab_set()                                # Bloquea la interacción con la ventana principal
    ajustes.resizable(False, False)                   # Desactiva el cambio de tamaño de la ventana

    # Vista de pestañas
    tabs = customtkinter.CTkTabview(ajustes)
    apariencia_name = TRADUCCIONES[idioma]["apariencia"]
    tabs.add(apariencia_name)               # Crea pestaña "Apariencia"
    tabs.set(apariencia_name)               # La selecciona como pestaña activa
    tab_actual = tabs.tab(apariencia_name)  # Contenedor interno de la pestaña
    tabs.pack(fill="both", expand=True, padx=5, pady=10)
    tabs.tab(apariencia_name).grid_columnconfigure((0,1), weight=1)
    #TODO tabs.tab(apariencia_name).grid_rowconfigure((0,1,2,3,4,5), weight=1)
    
    # Cálculo del tamaño y centrado de la ventana de ajustes respecto a la principal
    w_root = ventana.winfo_width()  
    h_root = ventana.winfo_height()
    x_ajustes= 250
    y_ajustes= 300
    x_top = (w_root - x_ajustes) // 2  
    y_top = (h_root - y_ajustes) // 2

    # Aplica tamaño y posición a la ventana de ajustes
    ajustes.geometry(f"{x_ajustes}x{y_ajustes}+{x_top}+{y_top}") 
    
    # --- Switch modo claro / oscuro ---
    # Detecta el modo de apariencia actual
    modo = True if customtkinter.get_appearance_mode() == "Dark" else False
    switch_var = customtkinter.BooleanVar(value=modo) 
    # Icono según modo actual
    texto = "🌙" if modo else "☀️"
    # Crea el switch de modo oscuro/claro
    modoOscuro = customtkinter.CTkSwitch(tab_actual, command=lambda: cambio_switch(modoOscuro, canvas, mapa, camino_anim, RES), variable=switch_var, text=texto, switch_width=60, switch_height=30, font=fuentes[0])
    modoOscuro.grid(row=0, column=0, padx=(0,30), pady=10, sticky="nse")
    
    # --- Label de formato de letra ---
    labelFormato = customtkinter.CTkLabel(tab_actual, text="Formato de letra:", font=fuentes[0])
    labels.append(labelFormato)  # Se añade a la lista para actualizarse al cambiar idioma
    labelFormato.grid(row=3, column=0, padx=2, pady=1, sticky="w")
    
    # --- Label de idioma ---
    labelIdioma = customtkinter.CTkLabel(tab_actual, text="Idioma:", font=fuentes[0])
    labels.append(labelIdioma)
    labelIdioma.grid(row=1, column=0, padx=2, pady=1, sticky="w")
    
    # --- Selector de idioma (SegmentedButton) ---
    # Variable ligada al idioma seleccionado actualmente
    idioma_var = customtkinter.StringVar(value=TRADUCCIONES[idioma]["idiomas"][IDIOMAS.index(idioma)])
    # Botón segmentado con los idiomas disponibles en el idioma actual
    idiomaBoton = customtkinter.CTkSegmentedButton(tab_actual, values=TRADUCCIONES[idioma]["idiomas"], 
                                                   font=fuentes[0], variable=idioma_var) 
    # Cuando se haga clic en un idioma, se llama a cambio_idioma(...)
    idiomaBoton.configure(command=lambda value: cambio_idioma(ajustes, tabs, idiomaBoton, 
                                                            idiomaBoton.cget("values").index(idiomaBoton.get()), labels))
    idiomaBoton.grid(row=2, column=0, padx=2, pady=(0,20), sticky="ew")
    
    # --- Selector de tipografía (familia de fuente) ---
    tipo_var = customtkinter.StringVar(value=fuentes[0].cget("family"))
    selecc_tipografia = customtkinter.CTkOptionMenu(tab_actual, font=fuentes[0], 
                                                    values=["Roboto", "Arial", "Times New Roman"],
                                                    anchor="center", variable=tipo_var,
                                                    command=lambda value: cambio_tipografia(value, fuentes))
    selecc_tipografia.grid(row=4, column=0, padx=2, pady=(0,10), sticky="ew")
    
    # --- Selector de tamaño de tipografía ---
    tam_var = customtkinter.StringVar(value=fuentes[0].cget("size"))
    selecc_tamaño = customtkinter.CTkOptionMenu(tab_actual, font=fuentes[0], 
                                                anchor="center", variable=tam_var, 
                                                values=["10", "12", "14", "16", "18", "20"])
    selecc_tamaño.configure(command=lambda value: cambio_tamaño_tipografia(value, fuentes))
    selecc_tamaño.grid(row=5, column=0, padx=2, pady=(0,10), sticky="ew")
    
def cambio_switch(switch : customtkinter.CTkSwitch, canvas: customtkinter.CTkCanvas, mapa : Mapa, 
                  camino_animacion: list[Estacion], RES: tuple[int, int]):
    """
    Alterna entre modo claro y oscuro y actualiza el icono del switch.
    """
    if (switch.get() == 0):
        imagen_mapa_tk = mapa.dibujar_estaciones(RES[0], RES[1], False)
        canvas.delete("all")
        canvas.configure(background="grey92")
        canvas.create_image(0, 0, image=imagen_mapa_tk, anchor="nw")
        mapa.recuperar_recorrido(RES[0], RES[1], canvas, camino_animacion)
        customtkinter.set_appearance_mode("Light")
        switch.configure(text="☀️")
    else:
        imagen_mapa_tk = mapa.dibujar_estaciones(RES[0], RES[1], True)
        canvas.delete("all")
        canvas.configure(background="grey14")
        canvas.create_image(0, 0, image=imagen_mapa_tk, anchor="nw")
        mapa.recuperar_recorrido(RES[0], RES[1], canvas, camino_animacion)
        customtkinter.set_appearance_mode("Dark") 
        switch.configure(text="🌙")

def cambio_idioma(ajustes : customtkinter.CTkToplevel , tabs : customtkinter.CTkTabview, 
                  idiomaBoton : customtkinter.CTkSegmentedButton, idioma_new_pos : int, 
                  labels : list [customtkinter.CTkLabel]):
    """
    Cambia el idioma de la ventana de ajustes y actualiza las etiquetas
    de la ventana principal.
    """
    global idioma
    # Cambiar el texto de la pestaña de apariencia según el nuevo idioma
    tabs.rename(TRADUCCIONES[idioma]["apariencia"], TRADUCCIONES[IDIOMAS[idioma_new_pos]]["apariencia"])
    tabs.set(TRADUCCIONES[IDIOMAS[idioma_new_pos]]["apariencia"])
    
    # Actualizar la variable global de idioma actual
    idioma = IDIOMAS[idioma_new_pos]
    
    # Actualizar título de la ventana de ajustes
    ajustes.title(TRADUCCIONES[idioma]["titulo_ajustes"])
    
    # Actualizar los valores mostrados en el selector de idioma
    idiomaBoton.configure(values=TRADUCCIONES[idioma]["idiomas"])
    idiomaBoton.set(TRADUCCIONES[idioma]["idiomas"][idioma_new_pos])
    
    # Actualizar los textos de los labels de la ventana principal
    i = 0
    for key in TRADUCCIONES[idioma]:
            if key not in ["idiomas", "titulo_ajustes", "apariencia"]:
                labels[i].configure(text=TRADUCCIONES[idioma][key])
                i += 1
    

def cambio_tipografia(tipografia, fuentes: list[customtkinter.CTkFont]):
    """
    Cambia la familia tipográfica (fuente) de todas las fuentes usadas en la interfaz.
    """
    for fuente in fuentes:
        fuente.configure(family=tipografia)
        

def cambio_tamaño_tipografia(tamaño, fuentes: list[customtkinter.CTkFont]):
    """
    Cambia el tamaño de la tipografía principal y, si existe, de una fuente secundaria.
    """
    fuentes[0].configure(size=int(tamaño))
    # La segunda fuente, si se usa para títulos, se hace algo más grande
    fuentes[1].configure(size=int(tamaño)+15)
    fuentes[3].configure(size=int(tamaño) - 2)
