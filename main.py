import customtkinter
from estaciones import *
from networkx import astar_path
from motor.mapa import Mapa

mapa = Mapa()
mapa = mapa.set_mapa(ESTACIONES, LINEAS, CONEXIONES, TRANSBORDOS)


# TODO: Interfaz grafica

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"

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
                            
ventana = customtkinter.CTk()
ventana.geometry("1920x1080")
ventana.iconbitmap('Imagenes/Logo_metro.ico')
ventana.title("Metro Ciudad de Mexico")
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_rowconfigure(0, weight=1)

entry_hora = customtkinter.StringVar(ventana, "")
entry_min = customtkinter.StringVar(ventana, "")
estaciones_names = [getattr(e, "nombre") for e in ESTACIONES]

# TODO:Color Provisional 
frameTexto = customtkinter.CTkFrame(ventana, width=1000 , height=1080, fg_color="grey19")
frameTexto.grid(row=0, column=0, sticky="nsw")

frameOrigen_Destino = customtkinter.CTkFrame(frameTexto, width=500, height=200, fg_color=frameTexto.cget("fg_color"))
frameOrigen_Destino.grid(row=0, column=0, pady=(20,0), padx=20, sticky="nw")

etiqOrigen = customtkinter.CTkLabel(frameOrigen_Destino, text="Origen:")
etiqOrigen.grid(row=0, column=0, padx=7, sticky="w")
etiqDestino = customtkinter.CTkLabel(frameOrigen_Destino, text="Destino:")
etiqDestino.grid(row=0, column=1, padx=7, sticky="w")

# # origen.pack(side="left", anchor="nw", padx=10, pady=20)
origen = customtkinter.CTkOptionMenu(frameOrigen_Destino, values=estaciones_names)
origen.grid(row=1, column=0, sticky="w")

destino = customtkinter.CTkOptionMenu(frameOrigen_Destino, values=estaciones_names)
destino.grid(row=1, column=1, sticky="w")



frameEntryTiempo = customtkinter.CTkFrame(frameTexto, width=500, height=200, fg_color=frameTexto.cget("fg_color"))
frameEntryTiempo.grid_columnconfigure(2, weight=1)
frameEntryTiempo.grid(row=1, column=0, padx=20, pady=20, sticky="nw")

etiqSalida = customtkinter.CTkLabel(frameEntryTiempo, text="Hora de salida (HH:MM):")
etiqSalida.grid(row=0, column=0, columnspan = 3, sticky="ew")

hora = customtkinter.CTkEntry(frameEntryTiempo, width=50, height=20, placeholder_text="00", textvariable=entry_hora)
hora.grid(row=1, column=0, sticky="w")
entry_hora.trace("w", lambda *args: character_limit_hour(entry_hora))

dosPuntos = customtkinter.CTkLabel(frameEntryTiempo, text=":")
dosPuntos.grid(row=1, column=1, sticky="w")

minuto = customtkinter.CTkEntry(frameEntryTiempo, width=50, height=20, placeholder_text="00", textvariable=entry_min)
minuto.grid(row=1, column=2, padx=1, sticky="w")
entry_min.trace("w", lambda *args: character_limit_min(entry_min))


framePreferencias = customtkinter.CTkFrame(frameTexto, width=100, height=200, fg_color=frameTexto.cget("fg_color"))
framePreferencias.grid(row=2, column=0, padx=20, pady=(20))
etiqPreferencias = customtkinter.CTkLabel(framePreferencias, text="Preferencias de viaje:")
etiqPreferencias.grid(row=0, column=0, sticky="w")

opcion1 = customtkinter.CTkCheckBox(framePreferencias, text="Menos trasbordos")
opcion1.grid(row=1, column=0, pady= 5, sticky= "w")
opcion2 = customtkinter.CTkCheckBox(framePreferencias, text="Baja Movilidad")
opcion2.grid(row=2, column=0, sticky= "w", padx=(0,500))

# # img = Image.open("imagenes/lupa.png") 
# # img = img.resize((50, 50), Image.LANCZOS)  # Resize to fit button    ns q hace esto jeje
# # button_image = ImageTk.PhotoImage(img)
# # lupa = customtkinter.CTkButton(frameIzquierdaArriba, image=button_image)
# # lupa.image=button_image
# # lupa.grid(row=2, column=5, padx=10)

# # def ajustes(ventana):
# #     ajustes = customtkinter.CTkToplevel(ventana)
# #     ajustes.geometry("120"x"120")
# #     modoOscuro = customtkinter.CtkSwitch(ajustes, command=cambio_switch, text="Modo oscuro")
# #     modoOscuro.pack(ajustes)


frameMapa = customtkinter.CTkFrame(ventana, fg_color=ventana.cget("fg_color"))
frameMapa.grid(row=0, column=1, sticky="nsew")



ventana.mainloop()