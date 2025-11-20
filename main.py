import customtkinter
from estaciones import *
from networkx import astar_path
from motor.mapa import Mapa
from PIL import Image
from tiempo.tiempo import sumar_hora, sumar_minutos

mapa = Mapa()
mapa.set_mapa(ESTACIONES, LINEAS, CONEXIONES, TRANSBORDOS)


# TODO: Interfaz grafica

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"

def abrir_ajustes():
    ajustes = customtkinter.CTkToplevel(ventana)
    ajustes.title("Ajustes")
    ajustes.after(10, lambda: ajustes.focus_force()) # Hace que la ventana de ajustes esté por arriba
    ajustes.grab_set()                               # Hace que no se pueda interactuar con la ventana principal hasta cerrar esta
    ajustes.resizable(False, False)    
    # No permite cambiar tamaño de la ventana
    tabs = customtkinter.CTkTabview(ajustes)
    tabs.add("Ajustes")
    tabs.set("Ajustes")
    tabs.pack(fill="both", expand=True, padx=10, pady=10)
    tabs = customtkinter.CTkTabview(ajustes)
    tabs.add("Ajustes")
    tabs.set("Ajustes")
    tabs.pack(fill="both", expand=True, padx=10, pady=10)
    tabs.tab("Ajustes").grid_columnconfigure(0, weight=1)
    tabs.tab("Ajustes").grid_rowconfigure((0,1), weight=1)
    
    w_root = ventana.winfo_width()                   # Obtener tamaño y posición de la ventana principal
    h_root = ventana.winfo_height()
    x_top = (w_root - 240) // 2                      # Calcular posición centrada
    y_top = (h_root - 240) // 2
    ajustes.geometry(f"{240}x{240}+{x_top}+{y_top}") 
    
    modo = True if customtkinter.get_appearance_mode() == "Dark" else False
    switch_var = customtkinter.BooleanVar(value=modo) 
    texto = "Modo oscuro" if modo else "Modo claro"
    etiqueta_ajustes = customtkinter.CTkLabel(tabs.tab("Ajustes"), text=texto, font=fuente_base)
    etiqueta_ajustes.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
    modoOscuro = customtkinter.CTkSwitch(tabs.tab("Ajustes"), command=lambda: cambio_switch(modoOscuro, etiqueta_ajustes), variable=switch_var, text="", switch_width=60, switch_height=30)
    modoOscuro.grid(row=1, column=0, padx=(0,30), pady=10, sticky="nse")
    
def cambio_switch(switch, etiqueta):
    if (switch.get() == 0):
        customtkinter.set_appearance_mode("Light")
        etiqueta.configure(text="Modo claro")
    else:
        customtkinter.set_appearance_mode("Dark") 
        etiqueta.configure(text="Modo oscuro")

def buscar_rutas():
    origen_text = origen.get()
    destino_text = destino.get()
    menos_trasbordos = opcion1.get()
    baja_movilidad = opcion2.get()
    hora_salida = entry_hora.get() + ":" + entry_min.get()


# Funcion que permite escribir hora con formato correcto
def character_limit_hour(entry_text):
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
 
# Funcion que permite escribir minuto con formato correcto    
def character_limit_min(entry_text):
    if len(entry_text.get()) > 0:
        primerCar = entry_text.get()[0]
        segundoCar = entry_text.get()[1:2]
        if primerCar not in {"0", "1", "2", "3", "4", "5"}:
            entry_text.set("")
        elif segundoCar not in {"0", "1", "2", "3", "4", "5", "6","7","8","9"}:
            entry_text.set(primerCar)
        else:
            entry_text.set(entry_text.get()[:2])

def button_callback(hora, min, paso, modo):
    if modo:
        value = float(hora.get()) + paso
        if len(hora.get()) == 1:
            hora.set("0" + str(value))
        elif value >= 24:
            hora.set("00")
        else:
            hora.set(value % 24)
    else:
        value = float(min.get()) + paso
        if len(min.get()) == 1:
            min.set("0" + str(value))
        elif value >= 60:
            min.set("00")
            hora.set((hora.get()+ 1) % 24)
        elif value < 0:
            min.set("55")
            hora.set((hora.get()- 1) % 24)
        else:
            min.set(value)  
            
def hora_button_callback(entry_hora, entry_min, paso):
    (hora, min)= sumar_hora(entry_hora.get(), entry_min.get(), paso)
    entry_hora.set(hora)
    entry_min.set(min)

def min_button_callback(entry_hora, entry_min, paso):
    (hora, min)= sumar_minutos(entry_hora.get(), entry_min.get(), paso)
    entry_hora.set(hora)
    entry_min.set(min)
                
            
# -----------------
# Frame principal
# -----------------
ventana = customtkinter.CTk()
ventana.geometry("1200x800") 
#ventana.after(0, lambda: ventana.state("zoomed")) # solo funciona en Windows
ventana.iconbitmap('Imagenes/Logo_metro.ico')
ventana.title("Metro Ciudad de Mexico")
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)
ventana.grid_rowconfigure(0, weight=1)

fuente_base = customtkinter.CTkFont(family="Roboto", size=16) # Fuente base para los textos

estaciones_names = [e.nombre for e in ESTACIONES] # Lista con los nombres de las estaciones
estaciones_names.sort() # Ordena las estaciones alfabeticamente

# ------------------------
# Frame izquierdo (texto)
# ------------------------
frameTexto = customtkinter.CTkFrame(ventana, fg_color="grey19") # TODO:Color Provisional 
frameTexto.grid_columnconfigure(0, weight=1)
frameTexto.grid_rowconfigure(3, weight=1)
frameTexto.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# --------------------------------------------------
# # Frame borde (contiene todos los frames interiores)
# # --------------------------------------------------
# frameBorde = customtkinter.CTkFrame(frameTexto, fg_color="grey", corner_radius=0)
# frameBorde.grid_columnconfigure(0, weight=1)
# frameBorde.grid_rowconfigure(3, weight=1) # Para que el frame resultado crezca hasta el final
# frameBorde.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# -------------------------
# Frame origen y destino
# -------------------------
# TODO: Una esquina no redondeada por la puta cara
frameOrigen_Destino = customtkinter.CTkFrame(frameTexto, fg_color= "blue", corner_radius=6)
frameOrigen_Destino.grid_columnconfigure((0,1), weight=1)
frameOrigen_Destino.grid(row=0, column=0, sticky="nsew", pady=10)

etiqOrigen = customtkinter.CTkLabel(frameOrigen_Destino, text="Origen", font=fuente_base, corner_radius=6)
etiqOrigen.grid(row=0, column=0, padx=(0,18), sticky="ew")
etiqDestino = customtkinter.CTkLabel(frameOrigen_Destino, text="Destino", font=fuente_base, corner_radius=6)
etiqDestino.grid(row=0, column=1, padx=(0,18), sticky="ew")  

# TODO: No cambiar tamaño al cambiar la opcion. Mirar con combo box o scrollable frame + radio buttons
origen = customtkinter.CTkOptionMenu(frameOrigen_Destino, values=estaciones_names, font=fuente_base, anchor="center")
origen.grid(row=1, column=0, padx=5, sticky="ew")
destino = customtkinter.CTkOptionMenu(frameOrigen_Destino, values=estaciones_names, font=fuente_base, anchor="center")
destino.grid(row=1, column=1, padx=5, sticky="ew")

lupa_imagen = customtkinter.CTkImage(light_image=Image.open("Imagenes/lupa.png").resize((25, 25)), size=(25, 25)) # Botón lupa
botonBuscar = customtkinter.CTkButton(frameOrigen_Destino, image=lupa_imagen, text="", width=50, height=50, corner_radius=10)
botonBuscar.grid(row=0, column=2, rowspan=2, padx=10)

ajustes_imagen = customtkinter.CTkImage(light_image=Image.open("Imagenes/Ajustes_light.png").resize((25, 25)), dark_image=Image.open("Imagenes/Ajustes_dark.png").resize((25, 25)), size=(25, 25)) # Botón ajustes
botonAjustes = customtkinter.CTkButton(ventana, image=ajustes_imagen, text="", width=30, height=30, corner_radius=10, command=abrir_ajustes)
botonAjustes.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

# -------------------
# Frame entrada hora
# -------------------
frameEntryTiempo = customtkinter.CTkFrame(frameTexto, fg_color= "green")
frameEntryTiempo.grid_columnconfigure((0,2), weight=1)
frameEntryTiempo.grid(row=1, column=0, sticky="nsew", pady=10)

entry_hora = customtkinter.StringVar(ventana, "00") # Etiqueta y Entrys para la hora de salida
entry_min = customtkinter.StringVar(ventana, "00")

etiqSalida = customtkinter.CTkLabel(frameEntryTiempo, text="Hora de salida (HH:MM):", font=fuente_base)
etiqSalida.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0,5))


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
framePreferencias = customtkinter.CTkFrame(frameTexto, fg_color="red")
framePreferencias.grid_columnconfigure(0, weight=1)
framePreferencias.grid(row=2, column=0, sticky="nsew", pady=10)

etiqPreferencias = customtkinter.CTkLabel(framePreferencias, text="Preferencias de viaje:", font=fuente_base)
etiqPreferencias.grid(row=0, column=0, sticky="w", pady=(0,5))
opcion1 = customtkinter.CTkCheckBox(framePreferencias, text="Menos trasbordos", font=fuente_base)
opcion1.grid(row=1, column=0, sticky="w", pady=5)
opcion2 = customtkinter.CTkCheckBox(framePreferencias, text="Baja Movilidad", font=fuente_base)
opcion2.grid(row=2, column=0, sticky="w", pady=5)

#TODO: Imprimir imprimir busqueda en el frame resultado
# ----------------
# Frame resultado
# ----------------
frameResultado = customtkinter.CTkFrame(frameTexto, fg_color="purple")
frameResultado.grid_columnconfigure(0, weight=1)
frameResultado.grid(row=3, column=0, sticky="nsew", pady=10)

# -----------------------------
# Frame principal derecho (mapa)
# -----------------------------
frameMapa = customtkinter.CTkFrame(ventana, fg_color="yellow")
frameMapa.grid_columnconfigure(0, weight=1)
frameMapa.grid_rowconfigure(0, weight=1)
frameMapa.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

mapa_dibujo = mapa.dibujar_estaciones(750, 750)
mapaLabel = customtkinter.CTkLabel(frameMapa, image=customtkinter.CTkImage(mapa_dibujo,size=(750, 750)), text="")
mapaLabel.grid(row=0, column=0, sticky="nsew")

ventana.mainloop()