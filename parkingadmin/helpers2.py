import base64
from inference_sdk import InferenceHTTPClient
from .models import Conjunto_celdas, Celda
import io
import os
from PIL import Image, ImageDraw
from django.core.files.storage import FileSystemStorage


"Función que envía imagen a roboflow y devuelve cantidad espacios vacíos y ocupados"
def detectar_espacios_vacios_y_ocupados(ruta_imagen):
    CLIENTE = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="CCFwsIHLnUb20EkzCwtq"
    )


    with open(ruta_imagen,'rb') as archivo_imagen:
        base64_image = base64.b64encode(archivo_imagen.read()).decode('utf-8')

    resultado = CLIENTE.infer(base64_image, model_id="parking-space-ipm1b/4")
    arreglo_predicciones = resultado['predictions']
    return arreglo_predicciones




"""Función que elimina predicciones con confianza menor a umbral de confianza"""
def eliminar_predicciones_bajo_umbral(arreglo_predicciones):
    umbral_confianza = 0.30
    arreglo_predicciones_con_umbral = []
    for prediccion in arreglo_predicciones:
        if prediccion['confidence'] >= umbral_confianza:
            arreglo_predicciones_con_umbral.append(prediccion)

    return arreglo_predicciones_con_umbral




"Función que valida si la cantidad de predicciones es igual a la cantidad de celdas presentes en el conjunto de celdas"
def prediccion_valida(arreglo_predicciones,conjunto_celdas_id):

    conjunto_celdas = Conjunto_celdas.objects.get(cnj_id = conjunto_celdas_id)
    celdas = Celda.objects.filter(cld_conjunto_celdas_id = conjunto_celdas)
    cantidad_predicciones = len(arreglo_predicciones)
    cantidad_celdas = len(celdas)

    #Si hay igual cantidad de celdas que de predicciones
    if cantidad_predicciones == cantidad_celdas:
        return True
    
    return False




"""Función que organiza las predicciones de izquierda a derecha según coordenadas en eje x"""
def organizar_predicciones(arreglo_predicciones):
    arreglo_predicciones_ordenado = []

    while(len(arreglo_predicciones) != 0):
        i = 0
        numero_menor = 99999999
        indice_menor = int
        for prediccion in arreglo_predicciones:
            if prediccion['x'] < numero_menor:
                numero_menor = prediccion['x']
                indice_menor = i
            i += 1
        arreglo_predicciones_ordenado.append(arreglo_predicciones[indice_menor])
        del arreglo_predicciones[indice_menor]
    
    return arreglo_predicciones_ordenado





"""Función que pinta predicciones detectadas en imagen"""
def dibujar_predicciones(ruta_imagen,nombre_imagen,predicciones):
    # Cargar la imagen original
    imagen = Image.open(ruta_imagen)
    draw = ImageDraw.Draw(imagen)

    # Dibujar las predicciones
    for prediccion in predicciones:
        x_centro = prediccion['x']
        y_centro = prediccion['y']
        ancho = prediccion['width']
        alto = prediccion['height']

        # Calcular las coordenadas del rectángulo
        x0 = x_centro - ancho / 2
        y0 = y_centro - alto / 2
        x1 = x_centro + ancho / 2
        y1 = y_centro + alto / 2

        # Color basado en el estado
        color = 'red' if prediccion['class'] == 'occupied' else 'green'
        
        # Dibujar el rectángulo
        draw.rectangle([x0, y0, x1, y1], outline=color, width=3)

    # Guardar la imagen modificada en media usando FileSystemStorage
    fs = FileSystemStorage(location='media')
    nombre_imagen_procesada = f"{os.path.splitext(nombre_imagen)[0]}_procesada.png"
    
    # Guardar la imagen
    with fs.open(nombre_imagen_procesada, 'wb') as archivo_guardado:
        imagen.save(archivo_guardado, format="PNG")
    
    return nombre_imagen_procesada





"""Función que llama a las funciones anteriores para detectar espacios vacíos y devuelve arreglo con resultados de ejecución"""
def ejecucion_helpers2(ruta_imagen, nombre_imagen_conjunto_celdas, conjunto_celdas_id):

    arreglo_predicciones = detectar_espacios_vacios_y_ocupados(ruta_imagen)
    arreglo_predicciones = eliminar_predicciones_bajo_umbral(arreglo_predicciones=arreglo_predicciones)
    nombre_imagen_con_bnd_boxes = dibujar_predicciones(ruta_imagen = ruta_imagen, nombre_imagen = nombre_imagen_conjunto_celdas, predicciones = arreglo_predicciones) 
    #zona testing
    confianzas = [prediccion['confidence'] for prediccion in arreglo_predicciones]
    print(f'cantidad predicciones: {len(arreglo_predicciones)}')
    print(f'confianza predicciones: {confianzas}')
    #fin zona testing
    if prediccion_valida(arreglo_predicciones,conjunto_celdas_id):
        arreglo_predicciones = organizar_predicciones(arreglo_predicciones)
        return {'arreglo_predicciones':arreglo_predicciones,'cambiar_celdas':True,'nombre_imagen_con_bnd_boxes':nombre_imagen_con_bnd_boxes}
    
    else: 
        arreglo_predicciones = organizar_predicciones(arreglo_predicciones)
        return {'cambiar_celdas':False,'nombre_imagen_con_bnd_boxes':nombre_imagen_con_bnd_boxes,'arreglo_predicciones':arreglo_predicciones}






def contar_ocupados_desocupados(arreglo_predicciones):
    ocupados = 0
    desocupados = 0

    for prediccion in arreglo_predicciones:
        if prediccion['class'] == "occupied":
            ocupados += 1
        elif prediccion['class'] == "empty":
            desocupados += 1
    
    return ocupados,desocupados
        




{   'inference_id': '8d8bdbb9-48c1-4bca-806c-65ee372c3f5c', 
    'time': 0.044326021000415494, 
    'image': {'width': 864, 'height': 446}, 
    'predictions': [{'x': 659.5, 'y': 261.5, 'width': 213.0, 'height': 165.0, 'confidence': 0.9309672713279724, 'class': 'occupied', 'class_id': 1, 'detection_id': 'e196bbc7-74aa-4d28-bd1f-25174432e64b'}, {'x': 279.5, 'y': 260.0, 'width': 209.0, 'height': 162.0, 'confidence': 0.9039661884307861, 'class': 'occupied', 'class_id': 1, 'detection_id': 'd2ae9846-3939-4521-936d-8a994b6f4e84'}, {'x': 465.0, 'y': 308.5, 'width': 228.0, 'height': 71.0, 'confidence': 0.8027831315994263, 'class': 'empty', 'class_id': 0, 'detection_id': '36a17af8-d154-4958-8b4b-68a78098d01c'}, {'x': 816.0, 'y': 255.0, 'width': 94.0, 'height': 172.0, 'confidence': 0.7493643760681152, 'class': 'occupied', 'class_id': 1, 'detection_id': '38941ca1-b2e2-4589-ae91-80c907b9692a'}]}