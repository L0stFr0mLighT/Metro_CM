import customtkinter
from estaciones import ESTACIONES, LINEAS
import mapa

# TODO: Interfaz grafica

# mapa.dibujar_estaciones(ESTACIONES, LINEAS, 100, 100)

def character_limit_hour(entry_text):
    if len(entry_text.get()) > 0:
        primerCar = entry_text.get()[:1]
        segundoCar = entry_text.get()[1:2]
        if primerCar not in {"0", "1", "2"}:
            entry_text.set("")
        elif primerCar == "2" and segundoCar not in {"0", "1", "2", "3", "4"}:
            entry_text.set(entry_text.get()[:1])
        elif segundoCar not in {"0", "1", "2", "3", "4", "5", "6","7","8","9"}:
            entry_text.set(entry_text.get()[:1])
        
        entry_text.set(entry_text.get()[:2])
    
def character_limit_min(entry_text):
    if len(entry_text.get()) > 0:
        primerCar = entry_text.get()[:1]
        segundoCar = entry_text.get()[1:2]
        if primerCar not in {"0", "1", "2", "3", "4", "5"}:
            entry_text.set("")
        elif segundoCar not in {"0", "1", "2", "3", "4", "5", "6","7","8","9"}:
            entry_text.set(entry_text.get()[:1])
        
        entry_text.set(entry_text.get()[:2])
                            
ventana = customtkinter.CTk()
ventana.geometry("1920x1080")
ventana.title("Metro Ciudad de Mexico")
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_rowconfigure(0, weight=1)

entry_hora = customtkinter.StringVar(ventana, "")
entry_min = customtkinter.StringVar(ventana, "")

# TODO:Color Provisional 
frameIzquierda = customtkinter.CTkFrame(ventana, width=1000 , height=1080 , fg_color="white")
frameIzquierda.grid_rowconfigure(0, weight=1)
frameIzquierda.grid(row=0, column=0, sticky="nsw")

frameIzquierdaArriba = customtkinter.CTkFrame(frameIzquierda, width=1000, height=500, fg_color="black")
# frameIzquierdaArriba.grid_rowconfigure((1,2), weight=1)
frameIzquierdaArriba.grid_columnconfigure((2), weight=1)
frameIzquierdaArriba.grid(row=0, column=0, sticky= "nwse")

frameIzquierdaAbajo = customtkinter.CTkFrame(frameIzquierda, width= 1000, height=500, fg_color="grey")
frameIzquierdaAbajo.grid(row=1, column=0)

frameDerecha = customtkinter.CTkFrame(ventana, fg_color=ventana.cget("fg_color"))
# frameDerecha.pack(side="right", padx=20, fill="both", expand= False)

estaciones_names = [getattr(e, "nombre") for e in ESTACIONES]

origen = customtkinter.CTkOptionMenu(frameIzquierdaArriba, values=estaciones_names)
# origen.pack(side="left", anchor="nw", padx=10, pady=20)
origen.grid(row=1, column=0, sticky="w")

destino = customtkinter.CTkOptionMenu(frameIzquierdaArriba, values=estaciones_names)
# destino.pack(side="left", anchor="nw", padx=10, pady= 20)
destino.grid(row=1, column=2, sticky="w")

etiqOrigen = customtkinter.CTkLabel(frameIzquierdaArriba, text="Origen")
etiqOrigen.grid(row=0, column=0, padx=10, sticky="w")
etiqDestino = customtkinter.CTkLabel(frameIzquierdaArriba, text="Destino")
etiqDestino.grid(row=0, column=2, sticky="w")

hora = customtkinter.CTkEntry(frameIzquierdaArriba, width=50, height=20, placeholder_text="00", textvariable=entry_hora)
hora.grid(row=2, column=0, sticky="e")
entry_hora.trace("w", lambda *args: character_limit_hour(entry_hora))

dosPuntos = customtkinter.CTkLabel(frameIzquierdaArriba, text=":")
dosPuntos.grid(row=2, column=1, sticky="w")

minuto = customtkinter.CTkEntry(frameIzquierdaArriba, width=50, height=20, placeholder_text="00", textvariable=entry_min)
minuto.grid(row=2, column=2, sticky="w")
entry_min.trace("w", lambda *args: character_limit_min(entry_min))

opcion1 = customtkinter.CTkCheckBox(frameIzquierdaArriba, text="Menos trasbordos")
opcion1.grid(row=1, column=4)
opcion2 = customtkinter.CTkCheckBox(frameIzquierdaArriba, text="Adaptado para silla de ruedas")
opcion2.grid(row=1, column=5)

# img = Image.open("imagenes/lupa.png") 
# img = img.resize((50, 50), Image.LANCZOS)  # Resize to fit button    ns q hace esto jeje
# button_image = ImageTk.PhotoImage(img)
# lupa = customtkinter.CTkButton(frameIzquierdaArriba, image=button_image)
# lupa.image=button_image
# lupa.grid(row=2, column=5, padx=10)

# def ajustes(ventana):
#     ajustes = customtkinter.CTkToplevel(ventana)
#     ajustes.geometry("120"x"120")
#     modoOscuro = customtkinter.CtkSwitch(ajustes, command=cambio_switch, text="Modo oscuro")
#     modoOscuro.pack(ajustes)











ventana.mainloop()