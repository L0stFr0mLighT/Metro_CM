import customtkinter
from estaciones import *
from networkx import astar_path
from motor.mapa import Mapa
from PIL import Image

mapa = Mapa()
mapa.set_mapa(ESTACIONES, LINEAS, CONEXIONES, TRANSBORDOS)


# TODO: Interfaz grafica

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"

# def ajustes(ventana):
#     ajustes = customtkinter.CTkToplevel(ventana)
#     ajustes.geometry("120"x"120")
#     modoOscuro = customtkinter.CtkSwitch(ajustes, command=cambio_switch, text="Modo oscuro")
#     modoOscuro.pack(ajustes)

# Funcion que permite escribir hora con formato correcto
def character_limit_hour(entry_text):
    if len(entry_text.get()) > 0:
        primerCar = entry_text.get()[0]     # Coge el primer numero
        segundoCar = entry_text.get()[1:2]  # Coge el segundo numero
        if primerCar not in {"0", "1", "2"}: #Si no está en el rango de horas válidas, no saca nada
            entry_text.set("")
        elif primerCar == "2" and segundoCar not in {"0", "1", "2", "3"}: # Jia es gay
            entry_text.set("2")
        elif segundoCar not in {"0", "1", "2", "3", "4", "5", "6","7","8","9"}:
            entry_text.set(primerCar)
        
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
        
        entry_text.set(entry_text.get()[:2])

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
estaciones_names.sort()

# ------------------------
# Frame izquierdo (texto)
# ------------------------
frameTexto = customtkinter.CTkFrame(ventana, fg_color="grey19") # TODO:Color Provisional 
frameTexto.grid_columnconfigure(0, weight=1)
frameTexto.grid_rowconfigure(0, weight=1)
frameTexto.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# --------------------------------------------------
# Frame borde (contiene todos los frames interiores)
# --------------------------------------------------
frameBorde = customtkinter.CTkFrame(frameTexto, fg_color="grey", corner_radius=0)
frameBorde.grid_columnconfigure(0, weight=1)
frameBorde.grid_rowconfigure(3, weight=1) # Para que el frame resultado crezca hasta el final
frameBorde.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# -------------------------
# Frame origen y destino
# -------------------------
frameOrigen_Destino = customtkinter.CTkFrame(frameBorde, fg_color= "blue")
frameOrigen_Destino.grid_columnconfigure((0,1,2), weight=1)
frameOrigen_Destino.grid(row=0, column=0, sticky="nsew", pady=(10,10))

etiqOrigen = customtkinter.CTkLabel(frameOrigen_Destino, text="Origen:", font=fuente_base)
etiqOrigen.grid(row=0, column=0, padx=10, sticky="w")
etiqDestino = customtkinter.CTkLabel(frameOrigen_Destino, text="Destino:", font=fuente_base)
etiqDestino.grid(row=0, column=1, padx=10, sticky="w")

origen = customtkinter.CTkOptionMenu(frameOrigen_Destino, values=estaciones_names, font=fuente_base)
origen.grid(row=1, column=0, padx=5, sticky="ew")
destino = customtkinter.CTkOptionMenu(frameOrigen_Destino, values=estaciones_names, font=fuente_base)
destino.grid(row=1, column=1, padx=5, sticky="ew")

lupa_imagen = customtkinter.CTkImage(light_image=Image.open("Imagenes/lupa.png").resize((30, 30)), size=(30, 30)) # Botón lupa
botonBuscar = customtkinter.CTkButton(frameOrigen_Destino, image=lupa_imagen, text="", width=50, height=50)
botonBuscar.grid(row=0, column=2, rowspan=2, padx=10, sticky="e")

# -------------------
# Frame entrada hora
# -------------------
frameEntryTiempo = customtkinter.CTkFrame(frameBorde, fg_color= "green")
frameEntryTiempo.grid_columnconfigure((0,2), weight=1)
frameEntryTiempo.grid(row=1, column=0, sticky="nsew", pady=(10,10))

entry_hora = customtkinter.StringVar(ventana, "") # Etiqueta y Entrys para la hora de salida
entry_min = customtkinter.StringVar(ventana, "")

etiqSalida = customtkinter.CTkLabel(frameEntryTiempo, text="Hora de salida (HH:MM):", font=fuente_base)
etiqSalida.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0,5))

hora = customtkinter.CTkEntry(frameEntryTiempo, width=50, height=20,textvariable=entry_hora, font=fuente_base)
hora.grid(row=1, column=0, sticky="e", padx=5)
entry_hora.trace("w", lambda *args: character_limit_hour(entry_hora))
dosPuntos = customtkinter.CTkLabel(frameEntryTiempo, text=":", font=fuente_base)
dosPuntos.grid(row=1, column=1, sticky="ew")
minuto = customtkinter.CTkEntry(frameEntryTiempo,width=50, height=20, textvariable=entry_min, font=fuente_base)
minuto.grid(row=1, column=2, sticky="w", padx=5)
entry_min.trace("w", lambda *args: character_limit_min(entry_min))

# --------------------
# Frame Preferencias
# --------------------
framePreferencias = customtkinter.CTkFrame(frameBorde, fg_color="red")
framePreferencias.grid_columnconfigure(0, weight=1)
framePreferencias.grid(row=2, column=0, sticky="nsew", pady=(10,10))

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
frameResultado = customtkinter.CTkFrame(frameBorde, fg_color="purple")
frameResultado.grid_columnconfigure(0, weight=1)
frameResultado.grid(row=3, column=0, sticky="nsew", pady=(10,10))

# -----------------------------
# Frame principal derecho (mapa)
# -----------------------------
frameMapa = customtkinter.CTkFrame(ventana, fg_color="yellow")
frameMapa.grid_columnconfigure(0, weight=1)
frameMapa.grid_rowconfigure(0, weight=1)
frameMapa.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

mapa_dibujo = mapa.dibujar_estaciones(900, 900)
mapaLabel = customtkinter.CTkLabel(frameMapa, image=customtkinter.CTkImage(mapa_dibujo,size=(900,900)), text="")
mapaLabel.grid(row=0, column=0, sticky="nsew")

ventana.mainloop()