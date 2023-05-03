from vistas import Vista
from controladores import gestor_eventos 
from flask import render_template

class PagInicio(Vista):
    """Página de inicio en la ruta `/`. Muestra todos los eventos
    en orden cronológico.
    """
    rol_minimo = 0
    template = 'inicio.html'
    url = '/'
    
    def mostrar(self):
        return render_template(self.template,
                eventos=gestor_eventos.obtenerEventos())

