from modelos import db, Modelo

class Usuario(Modelo):
    """Definicion de la fila de la tabla de Usuarios"""
    usuario: str = db.Column(db.String(100), nullable=False)
    contrasenha: str = db.Column(db.String(100), nullable=False)
    rol: int = db.Column(db.Integer, nullable=False)
    nombre: str = db.Column(db.String(100), nullable=False)
    dni: str = db.Column(db.String(100), nullable=False)
    celular: str = db.Column(db.String(100), nullable=False)
