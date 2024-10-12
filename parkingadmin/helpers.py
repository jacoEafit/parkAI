import base64
from inference_sdk import InferenceHTTPClient
import cv2 
import re
import os
import easyocr
from django.core.files.storage import FileSystemStorage
import io
from django.core.files.base import ContentFile

#Crea un reader de easyocr
reader = easyocr.Reader(['en'])


"""Función que recorta la placa de un vehículo dada una imagen"""
def recortar_placa(ruta_imagen):
    CLIENT= InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="CCFwsIHLnUb20EkzCwtq" #Mi api key de roboflow
    )

    #Se pasa imagen a base64 para que el modelo de roboflow pueda realizar predicción
    with open(ruta_imagen, "rb") as imagen:
        imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')

    #Se realiza predicción de placas en la imagen
    resultado = CLIENT.infer(imagen_base64, model_id="license-plate-recognition-rxg4e/4")
    
    #Se recorta la imagen para que solo quede placa
    imagen = cv2.imread(ruta_imagen) 

    cantidad_predicciones = len(resultado['predictions'])
    if cantidad_predicciones == 1:#Si la cantidad de predicciones es igual a 1
        x = int(resultado['predictions'][0]['x'] - resultado['predictions'][0]['width']/2)
        y = int(resultado['predictions'][0]['y'] - resultado['predictions'][0]['height']/2)
        width = int(resultado['predictions'][0]['width'])
        height = int(resultado['predictions'][0]['height'])
        
        imagen_recortada = imagen[y:y + height, x:x + width]

        # Convierte la imagen de BGR a RGB
        imagen_recortada = cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2RGB)

        return imagen_recortada
    
    else:
        return ''





"""Función que guarda la imagen recortada en carpeta media y devuelve su ruta"""
def guardar_imagen_recortada(imagen_recortada,nombre_imagen_vehiculo):

    # Convertir la imagen de NumPy a un formato JPEG en memoria
    _, buffer = cv2.imencode('.jpg', imagen_recortada)
    imagen_bytes = io.BytesIO(buffer)

    #Subir imagen a /media:
    fs = FileSystemStorage(location='media') #Especifíca ubicación
    nombre_imagen_recorte_placa = fs.save(f'recorte_placa_{nombre_imagen_vehiculo}.jpg', ContentFile(imagen_bytes.getvalue())) 
    url_imagen_recorte_placa = fs.url(nombre_imagen_recorte_placa) #Obtiene la url del archivo para poder acceder a él

    return url_imagen_recorte_placa

    



"""Devuelve arreglo con textos detectados en recorte de placa"""
def extraer_textos_placa(imagen_placa):
    resultados = reader.readtext(imagen_placa,detail=0)# Se leen textos de la placa
    print(resultados)
    if not resultados:# Si no se encuentran textos
        return ['']
    return resultados# Si se encuentran textos




"""Función que quita las letras indeceadas de la placa"""
def quitar_letras_indeceadas(texto):
    
    if len(texto) > 6:# Verificar si tiene longitud diferente a 6
        i = 0
        indice_ultimo_caracter_numerico = None
        for caracter in texto:# Se toma el último caracter numérico del string
            if caracter.isdigit():
                indice_ultimo_caracter_numerico = i
            i += 1

        texto = texto[max(0, indice_ultimo_caracter_numerico - 5):indice_ultimo_caracter_numerico+1]

    return texto





"""Función que lee la placa de un vehículo dada una imagen"""
def limpiar_textos(textos):

    texto = textos[0]# Se obtiene solo el primer texto para evitar obtener ciudad o demás info en placa
    if texto != '':# Si se detectaron textos
        texto = textos[0]# Se obtiene solo el primer texto para evitar obtener ciudad o demás info en placa
        texto = re.sub(r'[^a-zA-Z0-9]', '', texto)# Eliminar símbolos y espacios
        texto = quitar_letras_indeceadas(texto)# Se termina de limpiar cadena quitando letras indeceadas
    
    return texto





"""Función que llama a todas las anteriores funciones para devolver texto de placa"""
def procesar_placa(ruta_imagen, nombre_imagen_vehiculo):

    recorte_placa = recortar_placa(ruta_imagen)# Detectar y hacer recorte placa
    if recorte_placa.any() == '':#Si no se identifica placa ó si se identifican más
        return ''
    
    url_imagen_recorte_placa = guardar_imagen_recortada(recorte_placa,nombre_imagen_vehiculo)# Guardar imagen recorte

    textos = extraer_textos_placa(recorte_placa)# Extraer textos
    texto_limpio = limpiar_textos(textos = textos)# Limpiar símbolos de texto

    #Se valida que placa si tenga estructura adecuada:
    if len(texto_limpio) == 6:
        primeros_tres = texto_limpio[0:3]
        siguientes_tres = texto_limpio[3:6]
        if not primeros_tres.isalpha() or not siguientes_tres.isdigit():
            texto_limpio = ''

    return texto_limpio.upper(), url_imagen_recorte_placa
