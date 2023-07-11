from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Ambiente
from pony import orm
from app import Controlador, route, obtenerTodo
from forms import FormCrearAmbiente, FormModificarAmbiente
from datetime import date

pag_ambientes = Blueprint('ambientes', __name__)

# Pagina de todos los ambientes
class Ambientes(Controlador):
    url = '/ambientes'
    template = 'ambientes/ambientes.html'
    
    def get(self):
        ambientes = orm.select(_ for _ in Ambiente).order_by(Ambiente.nombre)
        return render_template(self.template, ambientes=ambientes)

    def post(self):
        id_ambiente = request.form.get('eliminar')
        Ambiente[id_ambiente].delete()
        return redirect(self.url)

route(pag_ambientes, Ambientes)


class CrearAmbiente(Controlador):
    url = '/ambientes/crear'
    template = 'ambientes/crear.html'

    def get(self):
        form = FormCrearAmbiente()
        return render_template(self.template, url=self.url, form=form)

    def post(self):
        form = FormCrearAmbiente()
        if form.validate():
            # creamos nuevo ambiente
            ambiente = Ambiente(nombre=form.nombre.data,
                    aforo=form.aforo.data,
                    locacion=form.locacion.data)
            flash(f'Ambiente "{ambiente.nombre}" creado.')
            return redirect('/ambientes')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect('/ambientes/crear')

route(pag_ambientes, CrearAmbiente)

class ModificarAmbiente(Controlador):
    url = '/ambientes/modificar/<int:id_ambiente>'
    template = 'ambientes/modificar.html'

    def get(self, id_ambiente):
        form = FormModificarAmbiente()
        try:
            ambiente = Ambiente[id_ambiente]
        except:
            abort(404)

        # ponemos los datos del ambiente en el formulario 
        form.nombre.data = ambiente.nombre
        form.aforo.data = ambiente.aforo
        form.locacion.data = ambiente.locacion
        
        return render_template(self.template,
                url=f'/ambientes/modificar/{ambiente.get_pk()}',
                form=form, ambiente=ambiente)

    def post(self, id_ambiente):
        form = FormModificarAmbiente()
        if form.validate():
            try:
                ambiente = Ambiente[id_ambiente]
            except:
                abort(404)

            # actualizamos los datos del ambiente con los del formulario
            ambiente.nombre = form.nombre.data
            ambiente.aforo = form.aforo.data
            ambiente.locacion = form.locacion.data
            flash(f'Ambiente "{ambiente.nombre}" modificado.')
            return redirect('/ambientes')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/ambientes/modificar/{id_ambiente}.')

route(pag_ambientes, ModificarAmbiente)

