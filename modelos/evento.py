from modelos import db, Modelo

class Evento(Modelo):
    """Definición de la fila de la tabla Eventos"""
    nombre: str = db.Column(db.String(100), nullable=False)
    img: str = db.Column(db.String(100), nullable=False)
    fecha: str = db.Column(db.String(100), nullable=False)
    descripcion: str = db.Column(db.String(100), nullable=False)

