import base64
from inference_sdk import InferenceHTTPClient
import cv2 
import pytesseract
import re

# Configura la ruta del ejecutable de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

#Función que lee la placa de un vehículo dada una imagen
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

    x = int(resultado['predictions'][0]['x'] - resultado['predictions'][0]['width']/2)
    y = int(resultado['predictions'][0]['y'] - resultado['predictions'][0]['height']/2)
    width = int(resultado['predictions'][0]['width'])
    height = int(resultado['predictions'][0]['height'])
    
    imagen_recortada = imagen[y:y + height, x:x + width]

    # Convierte la imagen de BGR a RGB
    imagen_recortada = cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2RGB)

    return imagen_recortada



def extraer_texto_placa(imagen_placa):

    # Usa pytesseract para leer la placa
    plate_text = pytesseract.image_to_string(imagen_placa, config='--psm 8')
    return plate_text 


def eliminar_simbolos(string):
    # Usamos una expresión regular para mantener solo letras, números y espacios
    return re.sub(r'[^a-zA-Z0-9\s]', '', string)