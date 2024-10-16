import base64
from inference_sdk import InferenceHTTPClient
from .models import Conjunto_celdas, Celda


"""Función que envía imagen a roboflow y devuelve cantidad espacios vacíos y ocupados"""
def detectar_espacios_vacios_y_ocupados(ruta_imagen):
    CLIENTE = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="CCFwsIHLnUb20EkzCwtq"
    )


    with open(ruta_imagen,'rb') as archivo_imagen:
        base64_image = base64.b64encode(archivo_imagen.read()).decode('utf-8')

    resultado = CLIENTE.infer(base64_image, model_id="real-time-car-parking/4")
    return resultado



"""Función que valida si la cantidad de predicciones es igual a la cantidad de celdas presentes en el conjunto de celdas"""
def prediccion_valida(predicciones,conjunto_celdas_id):

    conjunto_celdas = Conjunto_celdas.objects.get(cnj_id = conjunto_celdas_id)
    celdas = Celda.objects.filter(cld_conjunto_celdas_id = conjunto_celdas)
    cantidad_predicciones = len(predicciones)
    cantidad_celdas = len(celdas)

    #Si hay igual cantidad de celdas que de predicciones
    if cantidad_predicciones == cantidad_celdas:
        return True
    
    return False




def modificar_estado_celdas(predicciones,conjunto_celdas_id):
    conjunto_celdas = Conjunto_celdas.objects.get(cnj_id = conjunto_celdas_id)
    celdas = Celda.objects.filter(cld_conjunto_celdas_id = conjunto_celdas)

    i = 0
    for celda in celdas:
        celda.cld_estado = predicciones[i]
        celda.save()
        print(celda.cld_estado)