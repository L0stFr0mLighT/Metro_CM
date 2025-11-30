
from common.estacion import Estacion, Linea
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
        "contenidoAcercaDe":"Programa creado por:\n\nPablo Regidor Mendez\nDaniel Ramon Gragera\nYurong Cheng\nYun Chen\nAlvaro Vicente Bonilla\nJia Jie Ye",
        "noExisteRuta": "No existe ruta entre las estaciones seleccionadas.",
        "resumenTitulo":"Resumen del trayecto",
        "detallesTitulo":"Detalle del recorrido",
        "detalles origen == destino":"Estas llendo a la misma estación.",
        "resumen":"Origen:  {0}\nDestino: {1}\nDuración total: {2} h, {3} min\nLlegada estimada: {4}:{5}",
        "detallesPrimerTramo": "• Toma la línea {0} en {1}.",
        "detallesSigue":"• Sigue en la línea {0} hasta {1}",
        "detallesLlegada":"• Llega a tu destino: {0}.",
        "detallesTransbordo": "• Haz transbordo de la línea {0} a la línea {1} en {2}",
        "formatoLetra": "Formato de letra:",
        "idioma": "Idioma:",
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
        "contenidoAcercaDe":"Programm created by:\n\nPablo Regidor Mendez\nDaniel Ramon Gragera\nYurong Cheng\nYun Chen\nAlvaro Vicente Bonilla\nJia Jie Ye",
        "noExisteRuta": "There isn't any route between the selected stations.",
        "resumenTitulo":"Summary of the route",
        "detallesTitulo":"Details of the route",
        "detalles origen == destino":"You are in the same station.",
        "resumen":"Beginning:  {}\nDestination: {}\nTotal time: {} h, {} min\nTime of arrival: {}:{}",
        "detallesPrimerTramo": "• Take the line {} on {}.",
        "detallesSigue":"• Continue on line {} until {}",
        "detallesLlegada":"• Reach your destination: {}.",
        "detallesTransbordo": "• Change lines from {} to {} on {}",
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
        "resultado": "Itinéraire optimal",
        "inicio": "Commencer",
        "ajustes": "Ajustements",
        "acercaDe": "À propos de",
        "cerrar": "Fermer",
        "contenidoAcercaDe":"Programme créé par:\n\nPablo Regidor Mendez\nDaniel Ramon Gragera\nYurong Cheng\nYun Chen\nAlvaro Vicente Bonilla\nJia Jie Ye",
        "noExisteRuta": "Il n'existe aucun itinéraire entre les stations sélectionnées.",
        "resumenTitulo":"Résumé du trajet",
        "detallesTitulo":"Détails du trajet",
        "detalles origen == destino":"Vous êtes à la même station.",
        "resumen":"Départ : {0}\nDestination : {1}\nDurée totale : {2} h, {3} min\nHeure d'arrivée : {4}:{5}",
        "detallesPrimerTramo": "• Prenez la ligne {0} à {1}.",
        "detallesSigue":"• Continuez sur la ligne {0} jusqu'à {1}",
        "detallesLlegada":"• Arrivée à destination : {0}.",
        "detallesTransbordo": "• Changez de la ligne {0} vers la ligne {1} à {2}",
        "formatoLetra": "Police format :",
        "idioma": "Langue:",
    }
}

IDIOMAS = ["Español", "Inglés", "Francés"]

def get_resumen(principales: list[tuple[Estacion, Linea | None]], tiempo_total, hora_estimada, idioma):
    if len(principales) == 0:
        return ""
    origen_est = principales[0][0]
    destino_est = principales[-1][0]
    
    resumen = TRADUCCIONES[idioma]["resumen"]
    resumen = resumen.format(origen_est.nombre, destino_est.nombre, tiempo_total[0], tiempo_total[1], hora_estimada[0], hora_estimada[1])
    return resumen

def get_texto_detalle(principales: list[tuple[Estacion, Linea | None]], idioma : str) -> str:
    pasos = []
    
    if len(principales) == 0:
        return ""
    origen_est = principales[0][0]
    destino_est = principales[-1][0]
    texto_detalle = ""
    # Buscar la primera línea NO None en el camino
    if(len(principales) < 2):    
        texto_detalle = TRADUCCIONES[idioma]["detalles origen == destino"]
        return texto_detalle
    else:
        # Primer tramo
        text = TRADUCCIONES[idioma]["detallesPrimerTramo"]
        pasos.append(text.format(principales[1][1].numero, origen_est.nombre))
    
    for i in range(1, len(principales) - 1):
            (est_a, linea_a) = principales[i] # Estación donde se transborda
            (est_b, linea_b) = principales[i + 1] # Estación destino del tramo siguiente

            # línea_a podría ser None en algún caso raro; lo ignoramos
            assert linea_a != None
            if est_a != est_b:
                # Sigue en la linea
                text = TRADUCCIONES[idioma]["detallesSigue"]
                pasos.append(text.format(linea_a.numero, est_b.nombre))
            elif linea_b == None:
                # Llegada
                text = TRADUCCIONES[idioma]["detallesLlegada"]
                pasos.append(text.format(destino_est.nombre))
            elif linea_a != linea_b:
                # Transbordo
                text = TRADUCCIONES[idioma]["detallesTransbordo"]
                pasos.append(text.format(linea_a.numero, linea_b.numero, est_a.nombre))
    texto_detalle = "\n".join(pasos)
    return texto_detalle