from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Vehiculo,Ingreso,Egreso,Organizacion,Parqueadero,Zona,Conjunto_celdas,Celda
from . import helpers
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.http import HttpResponse


def home(request):
    return render(request,'home.html')

def sobreNosotros(request):
    return render(request, 'sobreNosotros.html')

def lectura_placa_vehiculo(request):
    #Si ingresan una imagen 
    if request.method == 'POST' and request.FILES['image']:
        #Se obtiene imagen vehiculo desde templates:
        imagen_vehiculo = request.FILES['image']

        #Subir imagen a /media:
        fs = FileSystemStorage(location='media') #Especifíca ubicación
        nombre_imagen_vehiculo = fs.save(imagen_vehiculo.name, imagen_vehiculo) #Guarda imagen y almacena nombre archivo
        url_imagen_vehiculo = fs.url(nombre_imagen_vehiculo) #Obtiene la url del archivo para poder acceder a él


        #Se extrae placa vehiculo con visión artificial:
        resultados_procesamiento = helpers.procesar_placa(ruta_imagen = 'media/'+nombre_imagen_vehiculo, nombre_imagen_vehiculo = imagen_vehiculo.name)
        
        #Se valida si se obtuvo la placa correctamente
        if isinstance(resultados_procesamiento,tuple):#Si se detecto una placa
            placa_vhc_ingreso,url_imagen_recorte_placa = resultados_procesamiento
        else:
            placa_vhc_ingreso = resultados_procesamiento

        #Se valida si dicho vehículo existe:
        try:
            vehiculo = Vehiculo.objects.get(vhc_placa = placa_vhc_ingreso)
            vehiculo_existe = True
        except ObjectDoesNotExist:
            vehiculo_existe = False
        
        #Se crea el ingreso:
        #ingreso = Ingreso(ing_vehiculo_id = vehiculo.vhc_id, ing_placa_vehiculo = vehiculo.vhc_placa, ing_fecha_hora=timezone.now(), ing_imagen_vehiculo = 'imagenes_vehiculos/'+nombre_imagen_vehiculo)
        #ingreso.save()

        #Se renderiza nuevo template con respectivo contexto sobre nuevo ingreso
        context = {"vehiculo_existe":vehiculo_existe,"url_imagen_vehiculo":url_imagen_vehiculo,"url_imagen_recorte_placa":url_imagen_recorte_placa,"placa_vehiculo":placa_vhc_ingreso}
        return render(request,'lectura_placa_vehiculo.html',context=context)

    #Si no han ingresado imagen
    elif request.method == 'GET':
        return render(request,'lectura_placa_vehiculo.html')




"Vista que registra el ingreso del vehículo"
def ingreso_vehiculo(request):
    ruta_imagen_vehiculo = request.GET.get('url_imagen_vehiculo')
    placa = request.GET.get('placa')

    # Verificar si ambos parámetros fueron proporcionados
    if ruta_imagen_vehiculo and placa:
        #Se valida si dicho vehículo existe en base de datos:
        try:
            vehiculo = Vehiculo.objects.get(vhc_placa = placa)
        except ObjectDoesNotExist:
            return HttpResponse("Error: Esa placa no se encuentra registrada", status=400)

        nuevo_ingreso = Ingreso(ing_vehiculo_id = vehiculo, ing_placa_vehiculo=placa, ing_fecha_hora=timezone.now(), ing_imagen_vehiculo=ruta_imagen_vehiculo)
        nuevo_ingreso.save()
        context = {'ingreso':nuevo_ingreso}
        return render(request,'ingreso_succes.html',context=context)

    else: return HttpResponse("Error: No se obtuvieron correctamente los parámetros", status=400)




"Vista que registra el egreso del vehículo y genera cobro"
def egreso_vehiculo(request):
    ruta_imagen_vehiculo = request.GET.get('url_imagen_vehiculo')
    placa = request.GET.get('placa')

    # Verificar si ambos parámetros fueron proporcionados
    if ruta_imagen_vehiculo and placa:
        #Se valida si dicho vehículo existe en base de datos:
        try:
            vehiculo = Vehiculo.objects.get(vhc_placa = placa)
        except ObjectDoesNotExist:
            return HttpResponse("Error: Esa placa no se encuentra registrada", status=400)

        nuevo_egreso = Egreso(egr_vehiculo_id = vehiculo, egr_placa_vehiculo=placa, egr_fecha_hora=timezone.now(), egr_imagen_vehiculo=ruta_imagen_vehiculo)
        nuevo_egreso.save()
        context = {'egreso':nuevo_egreso}
        return render(request,'egreso_succes.html',context=context)

    else: return HttpResponse("Error: No se obtuvieron correctamente los parámetros", status=400)




"""Vista que permite el manejo de parqueaderos de cada usuario"""
def parking_management(request):
    #usuario = request.user
    #organizacion = Organizacion.objects.get(org_id = usuario)
    #parqueaderos = Parqueadero.objects.filter(prq_organizacion_id = organizacion)

    #parqueaderos = Parqueadero.objects.all()
    parqueaderos = ['parqueadero vegas','parqueadero regional1']
    context = {'parqueaderos':parqueaderos}
    return render(request,'parking_management.html',context = context)





def informacion_parqueadero(request,parqueadero_id):
    """
    parqueadero = Parqueadero.objects.get(prq_id = parqueadero_id)
    zonas = Zona.objects.filter(zna_parqueadero_id = parqueadero)

    info_zonas = [{
              'zona1':info_zona1,
              'conjunto_celdas':{'cjn1':[celda1,celda2,celda3],'cjn2':[celda4,celda5]}
              }]
    
    """




"""Vista para creación de parqueaderos"""
def crear_parqueadero(request):
    if request.method == "POST":
        nombre_parqueadero = request.POST.get('nombre_parqueadero')
        precio_dia = float(request.POST.get('precio_dia'))
        precio_hora = float(request.POST.get('precio_dia'))
        organizacion = Organizacion.objects.get(org_id = request.user)
        direccion = request.POST.get('direccion')
        return redirect(reverse('parking_management'))

    return render(request,'crear_parqueadero.html')

