from flask.views import MethodView
from pony import orm
from models import Evento

def route(blueprint, controller):
    blueprint.add_url_rule(controller.url,
            view_func=controller.as_view(controller.__name__))

def obtenerTodo(models, reverse=False):
    lista = list(orm.select(model for model in models if model.fecha_inicio is None))
    if reverse:
        lista += list(orm.select(model for model in models if model.fecha_inicio is not None) \
            .order_by(lambda model: orm.desc(model.fecha_inicio)))
    else:
        lista += list(orm.select(model for model in models if model.fecha_inicio is not None) \
            .order_by(lambda model: model.fecha_inicio))
    return lista

class Controlador(MethodView):
    init_every_request = False
