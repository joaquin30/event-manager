from pony.orm import *

# Acá esta declarado todo el modelo fisico del sistema

db = Database()

class Cuenta(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    usuario = Required(str, unique=True, index=True)
    contrasenha = Required(str)
    tipo = Required(str)

class Evento(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_caja = Optional('Caja', cascade_delete=True)
    st_paquetes = Set('Paquete')
    st_actividades = Set('Actividad')
    nombre = Required(str)
    descripcion = Required(str)
    fecha_inicio = Optional(str)
    fecha_fin = Optional(str)

class Actividad(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_evento = Required('Evento')
    fk_ambiente = Optional('Ambiente')
    st_paquetes = Set('Paquete')
    st_materiales = Set('Material')
    st_asistentes = Set('Inscrito')
    st_participantes = Set('Participante')
    nombre = Required(str, index=True)
    descripcion = Required(str)
    fecha_inicio = Required(str)
    fecha_fin = Required(str)

class Ambiente(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    set_actividades = Set('Actividad')
    nombre = Required(str, index=True, unique=True)
    aforo = Required(int)
    locacion = Required(str)

class Material(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_actividad = Required('Actividad')
    nombre = Required(str, index=True)
    cantidad = Required(int)

class Participante(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_actividad = Required('Actividad')
    nombre = Required(str)
    correo = Required(str)

class Paquete(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_evento = Required('Evento')
    st_actividades = Set('Actividad')
    st_inscritos = Set('Inscrito', reverse='st_inscrito_paquetes')
    st_preinscritos = Set('Inscrito', reverse='st_preinscrito_paquetes')
    nombre = Required(str, index=True)
    precio = Required(int)

class Caja(db.Entity):
    pk_id = PrimaryKey(int, auto=True)
    fk_evento = Required('Evento')
    st_comprobantes = Set('Comprobante')
    st_egresos = Set('Egreso')
    saldo = Required(int)

class Inscrito(db.Entity):
    pk_id = PrimaryKey(str, auto=True)
    st_inscrito_paquetes = Set('Paquete')
    st_preinscrito_paquetes = Set('Paquete')
    st_comprobantes = Set('Comprobante')
    st_actividades = Set('Actividad')
    nombre = Required(str)
    telefono = Required(str)
    correo = Required(str)

class Comprobante(db.Entity):
    pk_id = PrimaryKey(str)
    fk_caja = Required('Caja')
    fk_inscrito = Required('Inscrito')
    descripcion = Required(str)
    fecha_emision = Required(str, index=True)
    monto = Required(int)

class Egreso(db.Entity):
    pk_id = PrimaryKey(str)
    fk_caja = Required('Caja')
    descripcion = Required(str)
    fecha_emision = Required(str, index=True)
    monto = Required(int)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
