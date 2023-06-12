from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Actividad
from pony import orm
from app import Controlador, route, obtenerTodo
from forms import FormCrearActividad, FormModificarActividad, FormCrearPaquete

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
            evento.fecha_inicio = None
            evento.fecha_fin = None
        
        orm.commit()
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
        return render_template(self.template, evento=evento,
            form=form)

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
                
            actividad = Actividad(
                nombre=form.nombre.data,
                descripcion=form.descripcion.data,
                fecha_inicio=form.fecha_inicio.data,
                fecha_fin=form.fecha_fin.data,
                fk_evento=evento)

            if evento.fecha_inicio is None or evento.fecha_inicio > actividad.fecha_inicio:
                evento.fecha_inicio = actividad.fecha_inicio

            if evento.fecha_fin is None or evento.fecha_fin < actividad.fecha_fin:
                evento.fecha_fin = actividad.fecha_fin
            
            orm.commit()
            flash(f'Actividad "{ actividad.nombre }" creada.')
            return redirect(f'/actividades/{id_evento}')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/actividades/{id_evento}/crear')

route(pag_actividades, CrearActividad)

class ModificarActividad(Controlador):
    url = '/actividades/<int:id_evento>/modificar/<int:id_actividad>'
    template = 'actividades/modificar.html'

    def get(self, id_evento, id_actividad):
        form = FormModificarActividad()
        try:
            evento = Evento[id_evento]
            actividad = Actividad[id_actividad]
        except:
            abort(404)

        form.nombre.data = actividad.nombre
        form.descripcion.data = actividad.descripcion
        form.fecha_inicio.data = actividad.fecha_inicio
        form.fecha_fin.data = actividad.fecha_fin
        return render_template(self.template,
                url=f'/actividades/{id_evento}/modificar/{id_actividad}',
                form=form, actividad=actividad, evento=evento)

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

            actividad.nombre = form.nombre.data
            actividad.descripcion = form.descripcion.data
            actividad.fecha_inicio = form.fecha_inicio.data
            actividad.fecha_fin = form.fecha_fin.data
            if evento.fecha_inicio is None or evento.fecha_inicio > actividad.fecha_inicio:
                evento.fecha_inicio = actividad.fecha_inicio

            if evento.fecha_fin is None or evento.fecha_fin < actividad.fecha_fin:
                evento.fecha_fin = actividad.fecha_fin
                
            orm.commit()
            flash(f'Actividad "{ actividad.nombre }" modificada.')
            return redirect(f'/actividades/{id_evento}')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/actividades/{id_evento}/modificar/{id_actividad}')

route(pag_actividades, ModificarActividad)
