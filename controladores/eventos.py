from controladores import Controlador
from modelos import tabla_eventos, Evento

class GestorEventos(Controlador):
    """Gestor para recuperar información de
    cualquier evento o grupo de eventos o modificar o
    eliminar alguno.
    """

    def obtenerEventos(self) -> list[Evento]:
        """Obtiene todos los eventos ordenados por su fecha
        en orden descendiente.
        
        **Retorno:** Una lista de eventos.
        """
        eventos = tabla_eventos.recuperarTodos()
        eventos.sort(key=lambda evento: evento.fecha, reverse=True)
        return eventos

    def obtenerEvento(self, id: int) -> Evento:
        """Obtiene un evento en especifico.

        **Argumentos:**

        - `id`: El identificador del evento.

        **Retorno:** Un objeto del modelo Evento o `None` si no se
        encontró algún evento con el identificador `id`.
        """
        if not tabla_eventos.existe(id):
            return None
        return tabla_eventos.recuperarUno(id)

