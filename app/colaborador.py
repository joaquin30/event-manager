from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Actividad, Ambiente, Participante, Material, Inscrito
from pony import orm
from app import *
from datetime import date

pag_colaborador = Blueprint('colaborador', __name__)

class Eventos(Controlador):
    template = 'colaborador/eventos.html'
    url = '/colaborador'

    def get(self):
        return render_template(self.template,
                eventos=obtenerTodo(Evento, reverse=True))

route(pag_colaborador, Eventos)


class Actividades(Controlador):
    template = 'colaborador/actividades.html'
    url = '/colaborador/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)
        
        return render_template(self.template, evento=evento,
                actividades=obtenerTodo(evento.st_actividades))
                
route(pag_colaborador, Actividades)


class Asistencia(Controlador):
    template = 'colaborador/asistencia.html'
    url = '/colaborador/<int:id_evento>/asistencia/<int:id_actividad>'

    def get(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)

        # recolectamos todos los inscritos de la actividad
        inscritos = []
        for paquete in actividad.st_paquetes:
            inscritos += list(paquete.st_inscritos)
        inscritos.sort(key=lambda x: x.nombre)
            
        return render_template(self.template, inscritos=inscritos, actividad=actividad)
                
    def post(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
            # añadimos el asistente a la lista de asistencia de la actividad
            id_asistente = request.form.get('asistente')
            print(id_asistente)
            actividad.st_asistentes.add(Inscrito[id_asistente])
            flash('Asistencia marcada')
        except:
            abort(404)
        
        return redirect(f'/colaborador/{id_evento}/asistencia/{id_actividad}')
    
route(pag_colaborador, Asistencia)


class Materiales(Controlador):
    template = 'colaborador/materiales.html'
    url = '/colaborador/<int:id_evento>/materiales/<int:id_actividad>'

    def get(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)
        
        return render_template(self.template, actividad=actividad,
                materiales=orm.select(_ for _ in actividad.st_materiales).order_by(Material.nombre))
                
    def post(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
            print('xd')
            # reducimos una unidad al material elegido
            id_material = request.form.get('material')
            count = Material[id_material].cantidad
            # para que la cantidad no sea negativa
            Material[id_material].cantidad = max(count-1, 0)
            flash('Material reducido en una unidad')
        except:
            abort(404)
        
        return redirect(f'/colaborador/{id_evento}/materiales/{id_actividad}')

route(pag_colaborador, Materiales)
