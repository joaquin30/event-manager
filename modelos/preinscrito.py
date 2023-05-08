from modelos import db, Modelo

class Preinscrito(Modelo):
    """Definicion de la fila de la tabla de Usuarios"""
    nombre: str = db.Column(db.String(100), nullable=False)
    edad: int = db.Column(db.Integer, nullable=False)
    telefono: str = db.Column(db.String(9), nullable=False)
    email: str = db.Column(db.String(100), nullable=False)
    evento_id: int = db.Column(db.Integer, nullable=False)

