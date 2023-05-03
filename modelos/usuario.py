from modelos import db, Modelo

class Usuario(Modelo):
    """Definicion de la fila de la tabla de Usuarios"""
    nombre: str = db.Column(db.String(100), nullable=False)
    contrasenha: str = db.Column(db.String(100), nullable=False)
    rol: int = db.Column(db.Integer, nullable=False)
