from django.shortcuts import render
from parkingadmin.models import Parqueadero, Zona, Celda
import random
from parkingadmin.decorators import sin_organizacion_required

# Create your views here.

def homeUsers(request):
    return render(request, 'homeUsers.html')


@sin_organizacion_required
def guiarUsuario(request):
        # Obtener todos los parqueaderos
    parqueaderos = Parqueadero.objects.all()
    
    if request.method == "POST":

        print("Método POST recibido")
        parqueadero_id = request.POST.get("parqueadero")
        print(f"ID de parqueadero seleccionado: {parqueadero_id}")
        parqueadero = Parqueadero.objects.get(prq_id=parqueadero_id)
        print(f"Parqueadero: {parqueadero.prq_nombre}")

        # Obtener todas las zonas de ese parqueadero
        zonas = Zona.objects.filter(zna_parqueadero_id=parqueadero)
        zonas_info = []

        # Para cada zona, contar cuántas celdas están vacías
        for zona in zonas:
            celdas_vacias = Celda.objects.filter(cld_conjunto_celdas_id__cnj_zona_id=zona, cld_estado='empty')

            zonas_info.append({
                'zona_nombre': zona.zna_nombre_zona,
                'celdas_vacias': celdas_vacias
            })

        # Si existen celdas vacías en alguna zona, seleccionamos una aleatoria
        celda_aleatoria = None
        if any(zona['celdas_vacias'] for zona in zonas_info):
            # Filtramos las celdas vacías de todas las zonas
            celdas_vacias_totales = [celda for zona in zonas_info for celda in zona['celdas_vacias']]
            celda_aleatoria = random.choice(celdas_vacias_totales)  # Elegir una celda aleatoria

        return render(request, "celdasDisponibles.html", {
            'parqueadero': parqueadero,
            'zonas_info': zonas_info,
            'celda_aleatoria': celda_aleatoria
        })
    
    return render(request, "guiarUsuario.html", {
        'parqueaderos': parqueaderos
    })

def sobreNosotrosUsers(request):
    return render(request, 'sobreNosotrosUsers.html')
