from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Actividad, Ambiente, Participante, Material
from pony import orm
from app import *
from forms import FormCrearActividad, FormModificarActividad, FormCrearParticipante, FormCrearMaterial
from datetime import date

pag_actividades = Blueprint('actividades', __name__)

class Eventos(Controlador):
    template = 'actividades/eventos.html'
    url = '/actividades'

    def get(self):
        return render_template(self.template,
                eventos=obtenerTodo(Evento, reverse=True))

route(pag_actividades, Eventos)


class Actividades(Controlador):
    template = 'actividades/actividades.html'
    url = '/actividades/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)
        
        return render_template(self.template, evento=evento,
                actividades=obtenerTodo(evento.st_actividades))
                
    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
            id_actividad = request.form.get('eliminar')
            Actividad[id_actividad].delete()
        except:
            abort(404)

        try:
            evento.fecha_inicio = min(act.fecha_inicio for act in evento.st_actividades)
            evento.fecha_fin = max(act.fecha_fin for act in evento.st_actividades)
        except:
            # eliminamos las fechas si es que ya no hay actividades
            evento.fecha_inicio = ''
            evento.fecha_fin = ''
        
        return redirect(f'/actividades/{id_evento}')
    

route(pag_actividades, Actividades)


class CrearActividad(Controlador):
    template = 'actividades/crear.html'
    url = '/actividades/<int:id_evento>/crear'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormCrearActividad()
        # obtenemos todos los ambientes para el autocompletado
        ambientes = orm.select(_ for _ in Ambiente).order_by(Ambiente.nombre)
        
        return render_template(self.template, evento=evento,
            form=form, ambientes=ambientes)

    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormCrearActividad()
        if form.validate():
            if form.fecha_inicio.data > form.fecha_fin.data:
                flash('La fecha de inicio es mayor a la fecha de fin.', 'error')
                return redirect(f'/actividades/{id_evento}/crear')

            # buscamos un ambiente que su nombre sea igual al del formulario
            ambiente_query = orm.select(amb for amb in Ambiente if amb.nombre == form.ambiente.data)
            if form.ambiente.data and len(ambiente_query) == 0:
                flash('No existe el ambiente.', 'error')
                return redirect(f'/actividades/{id_evento}/crear')

            actividad = Actividad(
                nombre=form.nombre.data,
                descripcion=form.descripcion.data,
                fecha_inicio=form.fecha_inicio.data.isoformat(), # convertimos date a str
                fecha_fin=form.fecha_fin.data.isoformat(),
                fk_evento=evento)

            if form.ambiente.data:
                # obtenemos el primer ambiente, que deberia ser el unico
                actividad.fk_ambiente = ambiente_query.first()

            # actualizamos la fecha de inicio y de fin del evento si es necesario
            if not evento.fecha_inicio or evento.fecha_inicio > actividad.fecha_inicio:
                evento.fecha_inicio = actividad.fecha_inicio

            if not evento.fecha_fin or evento.fecha_fin < actividad.fecha_fin:
                evento.fecha_fin = actividad.fecha_fin
            
            flash(f'Actividad "{ actividad.nombre }" creada.')
            return redirect(f'/actividades/{id_evento}')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/actividades/{id_evento}/crear')

route(pag_actividades, CrearActividad)

class ModificarActividad(Controlador):
    decorators = [login_required]
    url = '/actividades/<int:id_evento>/modificar/<int:id_actividad>'
    template = 'actividades/modificar.html'

    def get(self, id_evento, id_actividad):
        form = FormModificarActividad()
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)

        # cargamos todos los datos de la actividad de vuelta al formulario
        form.nombre.data = actividad.nombre
        if actividad.fk_ambiente:
            form.ambiente.data = actividad.fk_ambiente.nombre
            
        form.descripcion.data = actividad.descripcion
        form.fecha_inicio.data = date.fromisoformat(actividad.fecha_inicio)
        form.fecha_fin.data = date.fromisoformat(actividad.fecha_fin)

        # obtenemos los ambientes para el autocompletado
        ambientes = orm.select(_ for _ in Ambiente).order_by(Ambiente.nombre)
        
        return render_template(self.template,
                url=f'/actividades/{id_evento}/modificar/{id_actividad}',
                form=form, actividad=actividad, evento=evento, ambientes=ambientes)

    def post(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)

        form = FormCrearActividad()
        if form.validate():
            if form.fecha_inicio.data > form.fecha_fin.data:
                flash('La fecha de inicio es mayor a la fecha de fin.', 'error')
                return redirect(f'/actividades/{id_evento}/crear')
            
            ambiente_query = orm.select(amb for amb in Ambiente if amb.nombre == form.ambiente.data)
            if form.ambiente.data and len(ambiente_query) == 0:
                flash('No existe el ambiente.', 'error')
                return redirect(f'/actividades/{id_evento}/crear')

            # guardamos los datos del formulario en la actividad
            actividad.nombre = form.nombre.data
            actividad.ambiente = form.ambiente.data
            actividad.descripcion = form.descripcion.data
            actividad.fecha_inicio = form.fecha_inicio.data.isoformat()
            actividad.fecha_fin = form.fecha_fin.data.isoformat()
            if form.ambiente.data:
                actividad.fk_ambiente = ambiente_query.first()
            else:
                actividad.fk_ambiente = None

            # actualizamos las fechas, ya que posiblemente las hemos modificado
            evento.fecha_inicio = min(act.fecha_inicio for act in evento.st_actividades)
            evento.fecha_fin = max(act.fecha_fin for act in evento.st_actividades)
                
            flash(f'Actividad "{ actividad.nombre }" modificada.')
            return redirect(f'/actividades/{id_evento}')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/actividades/{id_evento}/modificar/{id_actividad}')

route(pag_actividades, ModificarActividad)


class Participantes(Controlador):
    decorators = [login_required]
    template = 'actividades/participantes.html'
    url = '/actividades/<int:id_evento>/participantes/<int:id_actividad>'

    def get(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)
        
        return render_template(self.template, evento=evento, actividad=actividad,
                participantes=orm.select(_ for _ in actividad.st_participantes).order_by(Participante.nombre))
                
    def post(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
            # eliminamos al participante
            id_participante = request.form.get('eliminar')
            Participante[id_participante].delete()
        except:
            abort(404)
        
        return redirect(f'/actividades/{id_evento}/participantes/{id_actividad}')
    

route(pag_actividades, Participantes)


class CrearParticipante(Controlador):
    decorators = [login_required]
    template = 'actividades/crear_participante.html'
    url = '/actividades/<int:id_evento>/participantes/<int:id_actividad>/crear'

    def get(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)

        form = FormCrearParticipante()
        return render_template(self.template, evento=evento,
            form=form, actividad=actividad)

    def post(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)

        form = FormCrearParticipante()
        if form.validate():
            # creamos un nuevo participante
            participante = Participante(
                nombre=form.nombre.data,
                correo=form.correo.data,
                fk_actividad=actividad)

            flash(f'Participante "{ participante.nombre }" creado.')
            return redirect(f'/actividades/{id_evento}/participantes/{id_actividad}')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/actividades/{id_evento}/participantes/{id_actividad}/crear')

route(pag_actividades, CrearParticipante)

# Basicamente un copy/paste de Participante
class Materiales(Controlador):
    decorators = [login_required]
    template = 'actividades/materiales.html'
    url = '/actividades/<int:id_evento>/materiales/<int:id_actividad>'

    def get(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)
        
        return render_template(self.template, evento=evento, actividad=actividad,
                materiales=orm.select(_ for _ in actividad.st_materiales).order_by(Material.nombre))
                
    def post(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
            # eliminamos al material
            id_material = request.form.get('eliminar')
            Material[id_material].delete()
        except:
            abort(404)
        
        return redirect(f'/actividades/{id_evento}/materiales/{id_actividad}')
    

route(pag_actividades, Materiales)


class CrearMaterial(Controlador):
    decorators = [login_required]
    template = 'actividades/crear_material.html'
    url = '/actividades/<int:id_evento>/materiales/<int:id_actividad>/crear'

    def get(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)

        form = FormCrearMaterial()
        return render_template(self.template, evento=evento,
            form=form, actividad=actividad)

    def post(self, id_evento, id_actividad):
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)

        form = FormCrearMaterial()
        if form.validate():
            # creamos un nuevo material
            material = Material(
                nombre=form.nombre.data,
                cantidad=form.cantidad.data,
                fk_actividad=actividad)

            flash(f'Material "{ material.nombre }" creado.')
            return redirect(f'/actividades/{id_evento}/materiales/{id_actividad}')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/actividades/{id_evento}/materiales/{id_actividad}/crear')

route(pag_actividades, CrearMaterial)
