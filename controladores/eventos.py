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
    
    def eliminarEvento(self, id: int):
        """Elimina un evento con el indentificador respectivo.
        
        **Argumentos**.

        - `id`: El identificador del evento

        """
        tabla_eventos.eliminar(id)

    def crearEvento(self, nombre: str, fecha: str, descripcion: str) -> int:
        """Crea un evento con los datos pasados en los argumentos.

        **Retorno:** el identificador de la nueva fila o -1 si es que la fila ya existia.
        """
        eventos = tabla_eventos.recuperarCuando(Evento.nombre == nombre)
        print(eventos)
        if len(eventos) > 0:
            return -1
        nuevo = Evento(nombre=nombre, fecha=fecha, descripcion=descripcion)
        tabla_eventos.insertar(nuevo)
        return nuevo.id
    
    def modificarEvento(self, id: int, nombre: str, fecha: str, descripcion: str):
        """Modifica el evento correspondiente al identificador con los datos de los argumentos.
        """
        evento = Evento(nombre=nombre, fecha=fecha, descripcion=descripcion)
        tabla_eventos.modificar(id, evento)

