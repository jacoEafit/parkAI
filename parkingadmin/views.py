from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Vehiculo,Ingreso,Egreso,Organizacion,Parqueadero,Zona,Conjunto_celdas,Celda
from . import helpers
from . import helpers2
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.http import HttpResponse
import json
from .decorators import organizacion_required


def home(request):
    return render(request,'home.html')

def sobreNosotros(request):
    return render(request, 'sobreNosotros.html')

@organizacion_required
def lectura_placa_vehiculo(request):
    #Si ingresan una imagen 
    if request.method == 'POST' and request.FILES['image']:
        #Se obtiene imagen vehiculo desde templates:
        imagen_vehiculo = request.FILES['image']

        #Subir imagen a /media:
        fs = FileSystemStorage(location='media') #Especifíca ubicación
        nombre_imagen_vehiculo = fs.save(imagen_vehiculo.name, imagen_vehiculo) #Guarda imagen y almacena nombre archivo
        url_imagen_vehiculo = fs.url(nombre_imagen_vehiculo) #Obtiene la url del archivo para poder acceder a él
        context = {'url_imagen_vehiculo':url_imagen_vehiculo}

        #Se extrae placa vehiculo con visión artificial:
        resultados_procesamiento = helpers.procesar_placa(ruta_imagen = 'media/'+nombre_imagen_vehiculo, nombre_imagen_vehiculo = imagen_vehiculo.name)
        
        #Se valida si se obtuvo la placa correctamente
        if resultados_procesamiento['se_detecto_una_placa'] == True and resultados_procesamiento['se_encontraron_textos'] == True: #Si se detecto una placa y texto en esa placa
            placa_vhc_ingreso = resultados_procesamiento['texto_detectado']
            url_imagen_recorte_placa = resultados_procesamiento['url_imagen_recorte_placa']
            #Se valida si dicho vehículo existe:
            try:
                vehiculo = Vehiculo.objects.get(vhc_placa = placa_vhc_ingreso)
                vehiculo_existe = True
            except ObjectDoesNotExist:
                vehiculo_existe = False
            context['vehiculo_existe'] = vehiculo_existe
            context['placa_vehiculo'] = placa_vhc_ingreso
            context['url_imagen_recorte_placa'] = url_imagen_recorte_placa

        elif resultados_procesamiento['se_detecto_una_placa'] == False and resultados_procesamiento['se_encontraron_textos'] == False: #Si no se detecta placa o más de una
            context['error_prediccion'] = "Error, no se detectaron placas ó se detectó más de una"
        
        elif resultados_procesamiento['se_detecto_una_placa'] == True and resultados_procesamiento['se_encontraron_textos'] == False: #Si se detecta placa pero no texto
            context['error_prediccion'] = "Error, no se detectó texto en la placa"

        

        #Se renderiza nuevo template con respectivo contexto sobre nuevo ingreso
        return render(request,'lectura_placa_vehiculo.html',context=context)

    #Si no han ingresado imagen
    elif request.method == 'GET':
        return render(request,'lectura_placa_vehiculo.html')




"Vista que registra el ingreso del vehículo"
@organizacion_required
def ingreso_vehiculo(request):

    #Se obtiene información del ingreso
    organizacion = Organizacion.objects.get(org_id = request.user)
    parqueadero = Parqueadero.objects.get(prq_organizacion_id = organizacion)
    nombre_parqueadero = parqueadero.prq_nombre
    ruta_imagen_vehiculo = request.GET.get('url_imagen_vehiculo')
    placa = request.GET.get('placa')

    # Verificar si ambos parámetros fueron proporcionados
    if ruta_imagen_vehiculo and placa:
        #Se valida si dicho vehículo existe en base de datos:
        try:
            vehiculo = Vehiculo.objects.get(vhc_placa = placa)
        except ObjectDoesNotExist:
            return HttpResponse("Error: Esa placa no se encuentra registrada", status=400)

        nuevo_ingreso = Ingreso(ing_vehiculo_id = vehiculo, ing_placa_vehiculo=placa, ing_parqueadero_id = parqueadero,ing_fecha_hora=timezone.now(), ing_imagen_vehiculo=ruta_imagen_vehiculo)
        nuevo_ingreso.save()
        context = {'ingreso':nuevo_ingreso,'nombre_parqueadero':nombre_parqueadero}
        return render(request,'ingreso_succes.html',context=context)

    else: return HttpResponse("Error: No se obtuvieron correctamente los parámetros", status=400)




"Vista que registra el egreso del vehículo y genera cobro"
@organizacion_required
def egreso_vehiculo(request):
    
    #Se obtiene información de egreso
    organizacion = Organizacion.objects.get(org_id = request.user)
    parqueadero = Parqueadero.objects.get(prq_organizacion_id = organizacion)
    nombre_parqueadero = parqueadero.prq_nombre
    ruta_imagen_vehiculo = request.GET.get('url_imagen_vehiculo')
    placa = request.GET.get('placa')

    # Verificar si ambos parámetros fueron proporcionados
    if ruta_imagen_vehiculo and placa:
        #Se valida si dicho vehículo existe en base de datos:
        try:
            vehiculo = Vehiculo.objects.get(vhc_placa = placa)
        except ObjectDoesNotExist:
            return HttpResponse("Error: Esa placa no se encuentra registrada", status=400)

        nuevo_egreso = Egreso(egr_vehiculo_id = vehiculo, egr_placa_vehiculo=placa, egr_parqueadero_id = parqueadero, egr_fecha_hora=timezone.now(), egr_imagen_vehiculo=ruta_imagen_vehiculo)
        nuevo_egreso.save()
        context = {'egreso':nuevo_egreso,'nombre_parqueadero':nombre_parqueadero}
        return render(request,'egreso_succes.html',context=context)

    else: return HttpResponse("Error: No se obtuvieron correctamente los parámetros", status=400)




"""Vista que permite el manejo de parqueaderos de cada usuario"""
@organizacion_required
def parking_management(request):
    usuario = request.user
    organizacion = Organizacion.objects.get(org_id = usuario)
    parqueaderos = Parqueadero.objects.filter(prq_organizacion_id = organizacion)

    context = {'parqueaderos':parqueaderos}
    return render(request,'parking_management.html',context = context)




@organizacion_required
def informacion_parqueadero(request,parqueadero_id):
    
    parqueadero = Parqueadero.objects.get(prq_id = parqueadero_id)
    zonas = Zona.objects.filter(zna_parqueadero_id = parqueadero)
    
    lista_zonas = []
    
    for zona in zonas:
        dic_zona = {
            'info_zona':zona,
            'conjunto_celdas':[]
        }

        #Obtener conjunto de celdas asociadas a zona
        conjunto_celdas = Conjunto_celdas.objects.filter(cnj_zona_id=zona)
        for cnj in conjunto_celdas:
            dic_cnj_celda = {
                'info_conjunto': cnj,
                'celdas':[]
            }

            #Obtener celdas asociadas a conjunto
            celdas = Celda.objects.filter(cld_conjunto_celdas_id = cnj)
            for celda in celdas:
                #Añadir celdas asociadas a conjunto de celda
                dic_cnj_celda['celdas'].append({'info_celda':celda})
            
            #Añadir conjunto de celdas a zona
            dic_zona['conjunto_celdas'].append(dic_cnj_celda)
        
        #Añadir zona a listado de zonas
        lista_zonas.append(dic_zona)

    return render(request,'informacion_parqueadero.html',{'parqueadero': parqueadero, 'info_zonas': lista_zonas})
    




"""Vista para creación de parqueaderos"""
@organizacion_required
def crear_parqueadero(request):
    if request.method == "POST":
        nombre_parqueadero = request.POST.get('nombre_parqueadero')
        precio_dia = float(request.POST.get('precio_dia'))
        precio_hora = float(request.POST.get('precio_dia'))
        organizacion = Organizacion.objects.get(org_id = request.user)
        direccion = request.POST.get('direccion')
        nuevo_parqueadero = Parqueadero(prq_nombre=nombre_parqueadero,prq_precio_dia=precio_dia,prq_precio_hora=precio_hora,prq_organizacion_id=organizacion,prq_direccion_parqueadero=direccion)
        nuevo_parqueadero.save()
        return redirect(reverse('parking_management'))

    return render(request,'crear_parqueadero.html')




"""Creación de conjunto de celdas. a cada conjunto de celdas le apuntará una cámara que validará cuantos parqueaderos se encuentran allí"""
@organizacion_required
def crear_zona(request,parqueadero_id):

    if request.method == "POST":
        parqueadero = Parqueadero.objects.get(prq_id = parqueadero_id)
        nombre_zona = request.POST.get('nombre_zona')
        nueva_zona = Zona(zna_parqueadero_id = parqueadero,zna_nombre_zona = nombre_zona)# Se crea el registro de la zona para el parqueadero indicado
        nueva_zona.save()
        return redirect('informacion_parqueadero',parqueadero_id = parqueadero_id)

    return render(request,'crear_zona.html')



@organizacion_required
def crear_conjunto_celdas(request,zona_id):

    if request.method == "POST":
        zona = Zona.objects.get(zna_id = zona_id)
        nombre_conjunto = request.POST.get('nombre_conjunto')

        #Se crea conjunto
        nuevo_conjunto = Conjunto_celdas(cnj_zona_id=zona,cnj_nombre_conjunto=nombre_conjunto)
        nuevo_conjunto.save()

        #Se crean celdas para dicho conjunto
        cantidad_celdas = int(request.POST.get('cantidad_celdas'))
        nombre_cnj = nuevo_conjunto.cnj_nombre_conjunto
        for i in range(cantidad_celdas):
            nombre_celda = f'{nombre_cnj[0].upper()}{i+1}'
            nueva_celda = Celda(cld_nombre_celda=nombre_celda, cld_conjunto_celdas_id = nuevo_conjunto, cld_estado='Desocupado')
            nueva_celda.save()

        parqueadero_id = zona.zna_parqueadero_id.prq_id
        return redirect('informacion_parqueadero',parqueadero_id = parqueadero_id)

    return render(request,'crear_conjunto_celdas.html')



@organizacion_required
def eliminar_parqueadero(request,parqueadero_id):
    parqueadero = Parqueadero.objects.get(prq_id = parqueadero_id)
    parqueadero.delete()
    return redirect('parking_management')



@organizacion_required
def eliminar_zona(request,zona_id):
    zona = Zona.objects.get(zna_id = zona_id)
    parqueadero_id = zona.zna_parqueadero_id.prq_id
    zona.delete()
    return redirect('informacion_parqueadero',parqueadero_id = parqueadero_id)



@organizacion_required
def eliminar_conjunto_celdas(request,conjunto_celdas_id):
    conjunto_celdas = Conjunto_celdas.objects.get(cnj_id = conjunto_celdas_id)
    zona = conjunto_celdas.cnj_zona_id
    parqueadero_id = zona.zna_parqueadero_id.prq_id
    conjunto_celdas.delete()
    return redirect('informacion_parqueadero',parqueadero_id = parqueadero_id)



@organizacion_required
def validar_disponibilidad_celdas(request,conjunto_id):
    conjunto = Conjunto_celdas.objects.get(cnj_id = conjunto_id)

    if request.method == 'POST' and request.FILES['imagen_conjunto_celdas']:
        #Se obtiene imagen de conjunto celdas desde templates:
        imagen_conjunto_celdas = request.FILES['imagen_conjunto_celdas']
        #Subir imagen a /media:
        fs = FileSystemStorage(location='media') #Especifíca ubicación
        nombre_imagen_conjunto_celdas = fs.save(imagen_conjunto_celdas.name, imagen_conjunto_celdas) #Guarda imagen y almacena nombre archivo
        url_imagen_conjunto_celdas = fs.url(nombre_imagen_conjunto_celdas) #Obtiene la url del archivo para poder acceder a él
        context = {'url_imagen_conjunto_celdas':url_imagen_conjunto_celdas, 'conjunto':conjunto}

        #Procesamiento de la imagen para detección de espacios vacíos:
        resultados_ejecucion_prediccion = helpers2.ejecucion_helpers2(ruta_imagen = 'media/'+nombre_imagen_conjunto_celdas, nombre_imagen_conjunto_celdas=nombre_imagen_conjunto_celdas,conjunto_celdas_id=conjunto_id)

        #Si resultados de predicción son válidos:
        if resultados_ejecucion_prediccion['cambiar_celdas'] == True:
            arreglo_predicciones = resultados_ejecucion_prediccion['arreglo_predicciones']#Se obtienen predicciones
            context['resultado_ejecucion'] = "prediccion_valida"
            context['arreglo_predicciones'] = arreglo_predicciones
        else:
            context['resultado_ejecucion'] = "prediccion_erronea"

        #Se obtiene imagen con bnd_boxes:
        nombre_imagen_con_bnd_boxes = resultados_ejecucion_prediccion['nombre_imagen_con_bnd_boxes']
        url_imagen_con_bnd_boxes = fs.url(nombre_imagen_con_bnd_boxes)
        context['url_imagen_con_bnd_boxes'] = url_imagen_con_bnd_boxes

        #Se obtienen datos de predicción como cantidad celdas ocupadas y desocupadas:
        celdas_ocupadas, celdas_desocupadas = helpers2.contar_ocupados_desocupados(resultados_ejecucion_prediccion['arreglo_predicciones'])
        context['celdas_ocupadas'] = celdas_ocupadas
        context['celdas_desocupadas'] = celdas_desocupadas
        return render(request,'validar_disponibilidad_celdas.html',context=context)

    context = {'conjunto':conjunto}
    return render(request,'validar_disponibilidad_celdas.html',context=context)



@organizacion_required
def modificar_estado_celdas(request,conjunto_id,predicciones):
    
    # Decodifica el JSON de predicciones
    predicciones = json.loads(predicciones)

    conjunto_celdas = Conjunto_celdas.objects.get(cnj_id = conjunto_id)
    celdas = Celda.objects.filter(cld_conjunto_celdas_id = conjunto_celdas)
    zona = Zona.objects.get(zna_id = conjunto_celdas.cnj_zona_id.zna_id)
    parqueadero = Parqueadero.objects.get(prq_id = zona.zna_parqueadero_id.prq_id) 

    #Se modifica el estado de las celdas
    i = 0
    for celda in celdas:
        celda.cld_estado = predicciones[i]['class']
        celda.save()
        print(celda.cld_estado)        
        i = i+1
    
    return redirect('informacion_parqueadero',parqueadero_id = parqueadero.prq_id)