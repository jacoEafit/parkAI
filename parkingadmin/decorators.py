from functools import wraps
from django.shortcuts import redirect

def organizacion_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verifica si el usuario tiene una instancia de 'Organizacion'
        if hasattr(request.user, 'organizacion'):
            return view_func(request, *args, **kwargs)
        else:
            # Redirige a una URL específica si el usuario no es de tipo organización
            return redirect('no_organizacion')
    return _wrapped_view

