import customtkinter

from estaciones import ESTACIONES, LINEAS
import mapa

mapa.dibujar_estaciones(ESTACIONES, LINEAS, 100, 100)

# TODO: Interfaz grafica

ventana = customtkinter.CTk()
ventana.geometry("1920x1080")
ventana.title("Metro Ciudad de Mexico")

# TODO:Color Provisional 
frameIzquierda = customtkinter.CTkFrame(ventana, width=1000 , height=1080 , fg_color="white")
frameIzquierda.pack_propagate(False)
frameIzquierda.pack(side="left", padx=20)

frameIzquierdaArriba = customtkinter.CTkFrame(frameIzquierda, width=1000, height=500, fg_color="black")
frameIzquierdaArriba.pack_propagate(False)
frameIzquierdaArriba.pack(side="top")

frameIzquierdaAbajo = customtkinter.CTkFrame(frameIzquierda, width= 1000, height=500, fg_color="grey")
frameIzquierdaAbajo.pack(side="bottom")

frameDerecha = customtkinter.CTkFrame(ventana, fg_color=ventana.cget("fg_color"))
frameDerecha.pack(side="right", padx=20)

# frameVacio = customtkinter.CTkFrame(frameIzquierdaAbajo, fg_color=transparent)
# frameVacio.pack()


estaciones_names = [getattr(e, "nombre") for e in ESTACIONES]

lupa = customtkinter.CTkButton(frameIzquierdaArriba, text="Buscar")
lupa.pack(side="right", padx=20, pady=20)

destino = customtkinter.CTkOptionMenu(frameIzquierdaArriba, values=estaciones_names)
destino.pack(side="right", anchor="nw", padx=10, pady= 20)

origen = customtkinter.CTkOptionMenu(frameIzquierdaArriba, values=estaciones_names)
origen.pack(side="left",anchor="nw", padx=10, pady=20)


ventana.mainloop()