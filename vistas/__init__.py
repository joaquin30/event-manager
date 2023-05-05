from flask.views import View

class Vista(View):
    """Clase abstracta de la interfaz, se instancia para crear páginas.
    """
    methods = ['GET', 'POST']
    init_every_request = False
    rol_minimo: int
    """Número entre 0 y 3 que indica el nivel de acceso de la página.
    
    **Niveles:**
    - 0: No es necesario login
    - 1: Colaborador
    - 2: Encargado de evento
    - 3: Administrador
    """

    template: str
    """Nombre de la plantilla que usará la página.
    """

    url: str
    """Ruta de la página en el navegador.
    """
    
    def dispatch_request(self, *args, **kwargs):
        return self.mostrar(*args, **kwargs)

    def mostrar(self, *args, **kwargs):
        """Renderiza la página usando la plantilla y los datos
        que requiera del controlador respectivo.

        **Argumentos:**
        - `*args, **kwargs`: Un número variable de argumentos que serán indicados en el atributo url.

        **Retorno**: HTML listo para mostrar en el navegador.
        """
        pass

from .inicio import *
from .public_evento import *
from .eventos import *

pags = [PagInicio, PagPublicEvento, PagEventos, PagCrearEvento,
        PagModificarEvento]
