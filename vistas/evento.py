from vistas import Vista
from controladores import gestor_eventos
from flask import abort, render_template

class PagEvento(Vista):
    """Página web en la ruta `/evento/<int:evento_id>`.
    Muestra la descripción de un solo evento, además de tener
    el formulario para preinscribirse.
    """

    rol_minimo = 0
    template = 'evento.html'
    url = '/evento/<int:evento_id>'
     
    def mostrar(self, evento_id: int) -> str:
        evento = gestor_eventos.obtenerEvento(evento_id)
        if evento is None:
            abort(404)
        return render_template(self.template,
                evento=evento)

