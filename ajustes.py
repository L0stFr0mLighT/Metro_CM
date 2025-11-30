import customtkinter

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
        "resultado": "Optimal routes",
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
        "resultado": "Itinéraires optimaux",
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

def abrir_ajustes(ventana: customtkinter.CTk, fuentes : list[customtkinter.CTkFont], labels : list[customtkinter.CTkLabel]):
    ajustes = customtkinter.CTkToplevel(ventana)
    ajustes.title(TRADUCCIONES[idioma]["titulo_ajustes"])
    ajustes.focus_force() # Hace que la ventana de ajustes esté por arriba
    ajustes.grab_set()                               # Hace que no se pueda interactuar con la ventana principal hasta cerrar esta
    ajustes.resizable(False, False)                  # No permite cambiar tamaño de la ventana
    
    tabs = customtkinter.CTkTabview(ajustes)
    apariencia_name = TRADUCCIONES[idioma]["apariencia"]
    tabs.add(apariencia_name)
    tabs.set(apariencia_name)
    tab_actual = tabs.tab(apariencia_name)
    tabs.pack(fill="both", expand=True, padx=5, pady=10)
    tabs.tab(apariencia_name).grid_columnconfigure((0,1), weight=1)
    # tabs.tab(apariencia_name).grid_rowconfigure((0,1,2,3,4,5), weight=1)
    
    w_root = ventana.winfo_width()                   # Obtener tamaño y posición de la ventana principal
    h_root = ventana.winfo_height()
    x_ajustes= 250
    y_ajustes= 300
    x_top = (w_root - x_ajustes) // 2                      # Calcular posición centrada
    y_top = (h_root - y_ajustes) // 2

    ajustes.geometry(f"{x_ajustes}x{y_ajustes}+{x_top}+{y_top}") 
    
    modo = True if customtkinter.get_appearance_mode() == "Dark" else False
    switch_var = customtkinter.BooleanVar(value=modo) 
    texto = "🌙" if modo else "☀️"
    modoOscuro = customtkinter.CTkSwitch(tab_actual, command=lambda: cambio_switch(modoOscuro), variable=switch_var, text=texto, switch_width=60, switch_height=30, font=fuentes[0])
    modoOscuro.grid(row=0, column=0, padx=(0,30), pady=10, sticky="nse")
    
    
    labelFormato = customtkinter.CTkLabel(tab_actual, text="Formato de letra:", font=fuentes[0])
    labels.append(labelFormato)
    labelFormato.grid(row=3, column=0, padx=2, pady=1, sticky="w")
    
    labelIdioma = customtkinter.CTkLabel(tab_actual, text="Idioma:", font=fuentes[0])
    labels.append(labelIdioma)
    labelIdioma.grid(row=1, column=0, padx=2, pady=1, sticky="w")
    
    idioma_var = customtkinter.StringVar(value=TRADUCCIONES[idioma]["idiomas"][IDIOMAS.index(idioma)])
    idiomaBoton = customtkinter.CTkSegmentedButton(tab_actual, values=TRADUCCIONES[idioma]["idiomas"], 
                                                   font=fuentes[0], variable=idioma_var) 
    idiomaBoton.configure(command=lambda value: cambio_idioma(ajustes, tabs, idiomaBoton, 
                                                            idiomaBoton.cget("values").index(idiomaBoton.get()), labels))
    idiomaBoton.grid(row=2, column=0, padx=2, pady=(0,20), sticky="ew")
    
    
    
    tipo_var = customtkinter.StringVar(value=fuentes[0].cget("family"))
    selecc_tipografia = customtkinter.CTkOptionMenu(tab_actual, font=fuentes[0], 
                                                    values=["Roboto", "Arial", "Times New Roman"],
                                                    anchor="center", variable=tipo_var,
                                                    command=lambda value: cambio_tipografia(value, fuentes))
    selecc_tipografia.grid(row=4, column=0, padx=2, pady=(0,10), sticky="ew")
    
    tam_var = customtkinter.StringVar(value=fuentes[0].cget("size"))
    selecc_tamaño = customtkinter.CTkOptionMenu(tab_actual, font=fuentes[0], 
                                                anchor="center", variable=tam_var, 
                                                values=["10", "12", "14", "16", "18", "20"])
    selecc_tamaño.configure(command=lambda value: cambio_tamaño_tipografia(value, fuentes))
    selecc_tamaño.grid(row=5, column=0, padx=2, pady=(0,10), sticky="ew")
    
def cambio_switch(switch):
    if (switch.get() == 0):
        customtkinter.set_appearance_mode("Light")
        switch.configure(text="☀️")
    else:
        customtkinter.set_appearance_mode("Dark") 
        switch.configure(text="🌙")

def cambio_idioma(ajustes : customtkinter.CTkToplevel , tabs : customtkinter.CTkTabview, 
                  idiomaBoton : customtkinter.CTkSegmentedButton, idioma_new_pos : int, 
                  labels : list [customtkinter.CTkLabel]):
    global idioma
    # Cambia el idioma de la pestaña de ajustes
    tabs.rename(TRADUCCIONES[idioma]["apariencia"], TRADUCCIONES[IDIOMAS[idioma_new_pos]]["apariencia"])
    tabs.set(TRADUCCIONES[IDIOMAS[idioma_new_pos]]["apariencia"])
    idioma = IDIOMAS[idioma_new_pos]
    ajustes.title(TRADUCCIONES[idioma]["titulo_ajustes"])
    idiomaBoton.configure(values=TRADUCCIONES[idioma]["idiomas"])
    idiomaBoton.set(TRADUCCIONES[idioma]["idiomas"][idioma_new_pos])
    
    
    
    # Cambia el idioma de la ventana principal
    i = 0
    for key in TRADUCCIONES[idioma]:
            if key not in ["idiomas", "titulo_ajustes", "apariencia"]:
                labels[i].configure(text=TRADUCCIONES[idioma][key])
                i += 1
    
# TODO
def cambio_tipografia(tipografia, fuentes: list[customtkinter.CTkFont]):
    for fuente in fuentes:
        fuente.configure(family=tipografia)
        
# TODO
def cambio_tamaño_tipografia(tamaño, fuentes: list[customtkinter.CTkFont]):
    fuentes[0].configure(size=int(tamaño))
    fuentes[1].configure(size=int(tamaño)+15)
