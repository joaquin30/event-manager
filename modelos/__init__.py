from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Modelo(db.Model):
    """La clase abstracta de los modelos
    """
    __abstract__ = True
    
    id = db.Column(db.Integer, nullable=False,
            primary_key=True, autoincrement=True)
    """El identificador que todas las tablas tienen
    """

class Tabla:
    """La clase Tabla instancia un modelo para realizar operaciones
    en las filas de la tabla de aquel modelo. Contiene todos los
    métodos necesarios para """
    
    modelo: Modelo
    """El Modelo a la que la tabla se refiere.
    Ejemplo: `tabla_usuario = Tabla(Usuario)`
    """

    def __init__(self, modelo):
        self.modelo = modelo

    def recuperarTodos(self) -> list[Modelo]:
        """Recupera todas las filas de la tabla.

        **Retorno:** Una lista con todas las filas.
        """
        return db.session.scalars(db.select(self.modelo)).all()

    def recuperarCuando(self, condicion: Modelo) -> list[Modelo]:
        """Recupera las filas de la tabla que cumpla la condición.
        
        **Retorno:** Una lista con las filas que cumplan la condición.
        """
        return db.session.scalars(db.select(self.modelo).where(condicion)).all()

    def recuperarUno(self, id: int) -> Modelo:
        """Recupera una sola fila que corresponda al identificador.
        Si no existe tal fila da un error, utilizar junto al método
        `existe` para evitar errores.

        **Argumentos:**

        - `id`: Un entero que identifica a la fila de la tabla.

        **Retorno:** Una sola fila de la tabla.
        """
        return self.recuperarCuando(self.modelo.id == id)[0]

    def existe(self, id: int):
        """Comprueba que exista una fila que corresponda al identificador.

        **Argumentos:**

        - `id`: Un entero que identifica a la fila de la tabla.

        **Retorno:** Un booleano que indique si existe tal fila.
        """
        return len(self.recuperarCuando(self.modelo.id == id)) > 0

    def insertar(self, nuevo: Modelo):
        """Inserta una nueva fila en la tabla creando un nuevo modelos.
        No es necesario usar el atributo `id` del modelo, ya que
        este se genera automáticamente.

        **Argumentos:**

        - `nuevo`: El nuevo modelo a ser insertado.

        """
        db.session.add(nuevo)
        db.session.commit()

    def eliminar(self, id: int):
        """Elimina una fila con el identificador respectivo, si no
        existe tal fila, no hace nada.

        **Argumentos:**

        - `id`: el identificador de la fila.
        """
        if self.existe(id):
            db.session.delete(self.recuperarUno(id))
            db.session.commit()

    def modificar(self, id: int, nuevo: Modelo):
        """Modifica una fila con el identificador respectivo, si no
        existe tal fila, no hace nada.

        **Argumentos:**

        - `id`: el identificador de la fila.
        - `nuevo`: los nuevos datos de la fila
        """
        if self.existe(id):
            self.eliminar(id)
            nuevo.id = id
            self.insertar(nuevo)

from .evento import Evento
from .usuario import Usuario
from .preinscrito import Preinscrito

tabla_usuarios = Tabla(Usuario)
tabla_eventos = Tabla(Evento)
