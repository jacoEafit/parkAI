"""
import base64
from inference_sdk import InferenceHTTPClient
from .models import Conjunto_celdas, Celda


"Función que envía imagen a roboflow y devuelve cantidad espacios vacíos y ocupados"
def detectar_espacios_vacios_y_ocupados(ruta_imagen):
    CLIENTE = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="CCFwsIHLnUb20EkzCwtq"
    )


    with open(ruta_imagen,'rb') as archivo_imagen:
        base64_image = base64.b64encode(archivo_imagen.read()).decode('utf-8')

    resultado = CLIENTE.infer(base64_image, model_id="real-time-car-parking/4")
    return resultado



"Función que valida si la cantidad de predicciones es igual a la cantidad de celdas presentes en el conjunto de celdas"
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


#Observación: predicciones van de derecha a izquierda.
{   'inference_id': '8d8bdbb9-48c1-4bca-806c-65ee372c3f5c', 
    'time': 0.044326021000415494, 
    'image': {'width': 864, 'height': 446}, 
    'predictions': [{'x': 659.5, 'y': 261.5, 'width': 213.0, 'height': 165.0, 'confidence': 0.9309672713279724, 'class': 'occupied', 'class_id': 1, 'detection_id': 'e196bbc7-74aa-4d28-bd1f-25174432e64b'}, {'x': 279.5, 'y': 260.0, 'width': 209.0, 'height': 162.0, 'confidence': 0.9039661884307861, 'class': 'occupied', 'class_id': 1, 'detection_id': 'd2ae9846-3939-4521-936d-8a994b6f4e84'}, {'x': 465.0, 'y': 308.5, 'width': 228.0, 'height': 71.0, 'confidence': 0.8027831315994263, 'class': 'empty', 'class_id': 0, 'detection_id': '36a17af8-d154-4958-8b4b-68a78098d01c'}, {'x': 816.0, 'y': 255.0, 'width': 94.0, 'height': 172.0, 'confidence': 0.7493643760681152, 'class': 'occupied', 'class_id': 1, 'detection_id': '38941ca1-b2e2-4589-ae91-80c907b9692a'}]}
"""