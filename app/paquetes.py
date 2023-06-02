from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Paquete, Actividad
from pony import orm
from app import Controlador, route, obtenerTodo
from forms import FormCrearPaquete, FormModificarPaquete

pag_paquetes = Blueprint('paquetes', __name__)

class Eventos(Controlador):
    template = 'paquetes/eventos.html'
    url = '/paquetes'

    def get(self):
        return render_template(self.template,
                eventos=obtenerTodo(Evento, reverse=True))

route(pag_paquetes, Eventos)


class Paquetes(Controlador):
    template = 'paquetes/paquetes.html'
    url = '/paquetes/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        if evento.st_actividades.count() == 0:
            flash('Cree actividades en este evento para administrar los paquetes')
            return redirect('/paquetes')

        paquetes = orm.select(pq for pq in Paquete).order_by(lambda pq: pq.precio)
        return render_template(self.template, evento=evento,
                paquetes=paquetes)
                
    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
            id_paquete = request.form.get('eliminar')
            Paquete[id_paquete].delete()
            orm.commit()
        except:
            abort(404)
        
        return redirect(f'/paquetes/{id_evento}')
    

route(pag_paquetes, Paquetes)

class CrearPaquete(Controlador):
    template = 'paquetes/crear.html'
    url = '/paquetes/<int:id_evento>/crear'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormCrearPaquete()
        actividades = orm.select(act for act in evento.st_actividades).order_by(lambda act: act.nombre)
        form.actividades.choices = [(act.get_pk(), act.nombre) for act in actividades]
        return render_template(self.template, evento=evento,
            form=form)

    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormCrearPaquete()
        actividades = orm.select(act for act in evento.st_actividades).order_by(lambda act: act.nombre)
        form.actividades.choices = [(act.get_pk(), act.nombre) for act in actividades]
        if form.validate():
            paquete = Paquete(
                nombre=form.nombre.data,
                precio=form.precio.data,
                fk_evento=evento)
            for id_actividad in form.actividades.data:
                paquete.st_actividades.add(Actividad[id_actividad])
            
            orm.commit()
            flash(f'Paquete "{ paquete.nombre }" creado.')
            return redirect(f'/paquetes/{id_evento}')
        else:
            flash('Errores en el formulario.')
            return redirect(f'/paquetes/{id_evento}/crear')

route(pag_paquetes, CrearPaquete)


class ModificarPaquete(Controlador):
    url = '/paquetes/<int:id_evento>/modificar/<int:id_paquete>'
    template = 'paquetes/modificar.html'

    def get(self, id_evento, id_paquete):
        try:
            evento = Evento[id_evento]
            paquete = Paquete[id_paquete]
        except:
            abort(404)

        form = FormModificarPaquete()
        form.nombre.data = paquete.nombre
        form.precio.data = paquete.precio
        actividades = orm.select(act for act in evento.st_actividades).order_by(lambda act: act.nombre)
        form.actividades.choices = [(act.get_pk(), act.nombre) for act in actividades]
        form.actividades.data = orm.select(act.pk_id for act in paquete.st_actividades)[:]
        return render_template(self.template, evento=evento,
            form=form, paquete=paquete)

    def post(self, id_evento, id_paquete):
        try:
            evento = Evento[id_evento]
            paquete = Paquete[id_paquete]
        except:
            abort(404)

        form = FormModificarPaquete()
        form.nombre.data = paquete.nombre
        form.precio.data = paquete.precio
        actividades = orm.select(act for act in evento.st_actividades).order_by(lambda act: act.nombre)
        form.actividades.choices = [(act.get_pk(), act.nombre) for act in actividades]
        if form.validate():
            paquete.nombre = form.nombre.data
            paquete.precio = form.precio.data
            paquete.st_actividades.clear()
            for id_actividad in form.actividades.data:
                paquete.st_actividades.add(Actividad[id_actividad])
                
            orm.commit()
            flash(f'Paquete "{paquete.nombre}" modificado.')
            return redirect(f'/paquetes/{id_evento}')
        else:
            flash('Errores en el formulario.')
            return redirect(f'/paquetes/{id_evento}/modificar/{id_paquete}')

route(pag_paquetes, ModificarPaquete)
