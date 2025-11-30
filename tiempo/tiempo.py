import math

def formatear_hora_min(hora: int, min: int) -> tuple[str, str]:
    """
    Formatea la hora y los minutos para que siempre tengan dos digitos
    """
    if hora < 10:
        hora_str = str("0{}".format(str(hora)))
    else:
        hora_str = str(hora)
    if min < 10:
        min_str = str("0{}".format(str(min)))
    else:
        min_str = str(min)
    return (hora_str, min_str)

def sumar_hora(hora: str, min: str, suma: int) -> tuple[str, str]:
    """
    Suma el valor de las horas (int) guardadas en 'suma' a unas horas (int) y minutos (int) dado
    """
    valor_hora = int(hora)
    nuevo_valor = (valor_hora + suma) % 24

    return formatear_hora_min(nuevo_valor, str_to_int(min))
    
def sumar_minutos(hora: str, min: str, suma: int) -> tuple[str, str]:
    """
    Suma el valor de los minutos (int) guardadas en 'suma' a unas horas(int) y minutos (str) dado
    """
    valor_min = str_to_int(min)
    valor_hora = int(hora)

    valor_min_raw = valor_min + suma
    
    horas_pasadas = math.floor( float(valor_min_raw)/60 )
    nueva_hora = (valor_hora + horas_pasadas) % 24
    nuevo_min = valor_min_raw % 60

    return formatear_hora_min(nueva_hora, nuevo_min)

def str_to_int(x):
    """
    Convierte una cadena a entero, devolviendo 0 si la cadena es vacia
    """
    if(x == ""):
        return 0
    return int(x)