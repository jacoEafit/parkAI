import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Elimina todas las imágenes de la carpeta media sin importar dónde estén guardadas'

    def handle(self, *args, **kwargs):
        # Definir la ruta a la carpeta media
        media_dir = settings.MEDIA_ROOT

        # Verificar si la carpeta existe
        if not os.path.exists(media_dir):
            self.stdout.write(self.style.ERROR(f'La carpeta media no existe: {media_dir}'))
            return

        # Contar cuántos archivos se eliminaron
        archivos_eliminados = 0

        # Recorrer todos los archivos en la carpeta media
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                # Obtener la extensión del archivo
                _, extension = os.path.splitext(file)
                
                # Verificar si es una imagen (puedes agregar más extensiones si es necesario)
                if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                    archivo_path = os.path.join(root, file)
                    try:
                        os.remove(archivo_path)
                        archivos_eliminados += 1
                        self.stdout.write(self.style.SUCCESS(f'Eliminado: {archivo_path}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error eliminando {archivo_path}: {str(e)}'))

        # Mostrar cuántos archivos se eliminaron
        if archivos_eliminados > 0:
            self.stdout.write(self.style.SUCCESS(f'{archivos_eliminados} imágenes eliminadas.'))
        else:
            self.stdout.write(self.style.WARNING('No se encontraron imágenes para eliminar.'))
