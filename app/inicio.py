from flask import render_template, Blueprint, abort, flash, redirect
from models import Evento, Inscrito, Paquete
from pony import orm
from forms import FormPreinscripcion
from app import Controlador, route, obtenerTodo

pag_inicio = Blueprint('inicio', __name__)

class Inicio(Controlador):
    url = '/'
    template = 'inicio/inicio.html'
    
    def get(self):
        eventos = orm.select(ev for ev in Evento if ev.fecha_inicio) \
            .order_by(lambda ev: orm.desc(ev.fecha_inicio))
        return render_template(self.template, eventos=eventos)

route(pag_inicio, Inicio)

# La pagina individual de un evento publico
class PublicacionEvento(Controlador):
    url = '/<int:id_evento>'
    template = 'inicio/evento.html'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormPreinscripcion()
        paquetes = orm.select(pq for pq in evento.st_paquetes)
        form.paquete.choices = [(pq.get_pk(), pq.nombre) for pq in paquetes]
        return render_template(self.template,
                    evento=evento, form=form,
                    actividades=obtenerTodo(evento.st_actividades))
    
    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormPreinscripcion()
        paquetes = orm.select(pq for pq in evento.st_paquetes)
        form.paquete.choices = [(pq.get_pk(), pq.nombre) for pq in paquetes]
        if form.validate():
            doc_identidad = form.doc_identidad.data
            inscrito = Inscrito.get(pk_id=doc_identidad)
            # Si el preinscrito no esta en la base de datos creamos uno nuevo
            if inscrito is None:
                inscrito = Inscrito(
                            pk_id=doc_identidad,
                            nombre=form.nombre.data,
                            telefono=form.telefono.data,
                            correo=form.correo.data)
            # Sino actualizamos sus datos con los nuevo ingresados
            else:
                inscrito.nombre = form.nombre.data
                inscrito.telefono = form.telefono.data
                inscrito.correo = form.correo.data

            # Si el preinscrito ya se registro a este evento
            for paquete in evento.st_paquetes:
                if inscrito in paquete.st_inscritos or inscrito in paquete.st_preinscritos:
                    flash('Ya te preinscribiste antes.', 'error')
                    return redirect(f'/{id_evento}')
            
            inscrito.st_preinscrito_paquetes.add(Paquete[form.paquete.data])
            flash('Preinscripción exitosa.')
        else:
            flash('Errores en el formulario.', 'error')

        return redirect(f'/{id_evento}')

route(pag_inicio, PublicacionEvento)
