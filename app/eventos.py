from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Caja
from pony import orm
from app import Controlador, route, obtenerTodo
from forms import FormCrearEvento
from datetime import date

pag_eventos = Blueprint('eventos', __name__)

# Pagina de todos los evento
class Eventos(Controlador):
    url = '/eventos'
    template = 'eventos/eventos.html'
    
    def get(self):
        return render_template(self.template,
                eventos=obtenerTodo(Evento))

    def post(self):
        id_evento = request.form.get('eliminar')
        Evento[id_evento].delete()
        return redirect(self.url)

route(pag_eventos, Eventos)


class CrearEvento(Controlador):
    url = '/eventos/crear'
    template = 'eventos/crear.html'

    def get(self):
        form = FormCrearEvento()
        return render_template(self.template, url=self.url, form=form)

    def post(self):
        form = FormCrearEvento()
        if form.validate():
            evento = Evento(nombre=form.nombre.data,
                    descripcion=form.descripcion.data)

            # Creamos una caja automaticamente
            evento.fk_caja = Caja(saldo=0, fk_evento=evento)
            orm.commit()
            
            # guardamos la imagen elegida
            img = form.img.data
            img.save(f'static/img/{evento.pk_id}.png')
            flash(f'Evento "{evento.nombre}" creado. Crea actividades para que se muestre en inicio.')
            return redirect('/eventos')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect('/eventos/crear')

route(pag_eventos, CrearEvento)


from forms import FormModificarEvento

class ModificarEvento(Controlador):
    url = '/eventos/modificar/<int:id_evento>'
    template = 'eventos/modificar.html'

    def get(self, id_evento):
        form = FormModificarEvento()
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        # ponemos los datos del evento en el formulario
        form.nombre.data = evento.nombre
        form.descripcion.data = evento.descripcion
        return render_template(self.template,
                url=f'/eventos/modificar/{id_evento}',
                form=form, evento=evento)

    def post(self, id_evento):
        form = FormModificarEvento()
        if form.validate():
            try:
                evento = Evento[id_evento]
            except:
                abort(404)

            evento.nombre = form.nombre.data
            evento.descripcion = form.descripcion.data
            
            # Si se subió una nueva imagen sobreescribimos sobre la antigua
            if form.img.data is not None:
                img = form.img.data
                img.save(f'static/img/{id_evento}.png')

            flash(f'Evento "{evento.nombre}" modificado.')
            return redirect('/eventos')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/eventos/modificar/{id_evento}.')

route(pag_eventos, ModificarEvento)

