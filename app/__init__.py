from flask.views import MethodView, request
from pony import orm
from models import Evento, Cuenta
from flask_simplelogin import login_required

class Controlador(MethodView):
    init_every_request = False
    decorators = [login_required]

# Usa el blueprint (modulo) para enrutar el controlador hacia su url
def route(blueprint, controller):
    blueprint.add_url_rule(controller.url,
            view_func=controller.as_view(controller.__name__))

# Obtiene todas las fila de una tabla ordenado por su fecha_inicio, siempre
# poniendo primero los que la fecha_inicio es NULL
# Solo funciona con tablas que tengan el atributo fecha_inicio
def obtenerTodo(Model, reverse=False):
    if not hasattr(Model, 'fecha_inicio'):
        raise RuntimeError(f'obtenerTodo: {Model} no tiene atributo fecha_inicio')
        
    lista = list(orm.select(model for model in Model if not model.fecha_inicio))
    if reverse:
        lista += list(orm.select(model for model in Model if model.fecha_inicio) \
            .order_by(lambda model: orm.desc(model.fecha_inicio)))
    else:
        lista += list(orm.select(model for model in Model if model.fecha_inicio) \
            .order_by(lambda model: model.fecha_inicio))
    
    return lista

# Funciones de ayuda para tratar con dinero
from math import modf
from decimal import Decimal

def decimalToInt(val):
    b, a = modf(val)
    return int(a*100 + b*100)

def intToDecimal(val):
    x = val % 100
    if x < 10:
        x = f'0{x}'
    return Decimal(f'{val//100}.{x}')

# Verifica que el usario sea un superusario
def es_superusuario(user):
    query = orm.select(cuenta for cuenta in Cuenta if cuenta.usuario == user)
    if len(query) == 0 or not query.first().superusuario:
        return "La cuenta no tiene rol de superusuario"


