from pony.orm import *
from datetime import date
from decimal import Decimal

db = Database()

class Cuenta(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    st_colaborador_eventos = Set('Evento', reverse='st_colaboradores')
    st_encargado_eventos = Set('Evento', reverse='st_encargados')
    usuario = Required(str)
    contrasenha = Required(str)
    superusuario = Optional(bool)

class Evento(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_caja = Optional('Caja', cascade_delete=True)
    st_colaboradores = Set('Cuenta')
    st_encargados = Set('Cuenta')
    st_paquetes = Set('Paquete')
    st_actividades = Set('Actividad')
    nombre = Required(str)
    descripcion = Required(str)
    fecha_inicio = Optional(date)
    fecha_fin = Optional(date)

class Actividad(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_evento = Required('Evento')
    fk_ambiente = Optional('Ambiente')
    st_materiales = Set('Material')
    st_paquetes = Set('Paquete')
    nombre = Required(str)
    descripcion = Required(str)
    fecha_inicio = Required(date)
    fecha_fin = Required(date)

class Ambiente(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    set_actividades = Set('Actividad')
    nombre = Required(str)
    aforo = Required(int)
    locacion = Required(str)

class Material(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_actividad = Required('Actividad')
    nombre = Required(str)
    cantidad = Required(int)

class Paquete(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_evento = Required('Evento')
    st_actividades = Set('Actividad')
    st_inscritos = Set('Inscrito', reverse='st_inscrito_paquetes')
    st_preinscritos = Set('Inscrito', reverse='st_preinscrito_paquetes')
    nombre = Required(str)
    precio = Required(Decimal)

class Caja(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_evento = Required('Evento')
    st_comprobantes = Set('Comprobante')
    st_egresos = Set('Egreso')
    saldo = Required(Decimal)

class Inscrito(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    st_inscrito_paquetes = Set('Paquete')
    st_preinscrito_paquetes = Set('Paquete')
    st_comprobantes = Set('Comprobante')
    nombre = Required(str)
    telefono = Required(str)
    correo = Required(str)

class Comprobante(db.Entity):
    pk_id = PrimaryKey(str)
    fk_caja = Required('Caja')
    fk_inscrito = Required('Inscrito')
    descripcion = Required(str)
    fecha_emision = Required(date)
    monto = Required(Decimal)

class Egreso(db.Entity):
    pk_id = PrimaryKey(str)
    fk_caja = Required('Caja')
    descripcion = Required(str)
    fecha_emision = Required(date)
    monto = Required(Decimal)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
