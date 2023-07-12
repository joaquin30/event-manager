from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Actividad, Ambiente, Participante, Material
from pony import orm
from app import *
from forms import FormComisionAgregarCuenta
from datetime import date

pag_comisiones = Blueprint('comisiones', __name__)

class Eventos(Controlador):
    template = 'comisiones/eventos.html'
    url = '/comisiones'

    def get(self):
        return render_template(self.template,
                eventos=obtenerTodo(Evento, reverse=True))

route(pag_comisiones, Eventos)


class Comision(Controlador):
    template = 'comisiones/comisiones.html'
    url = '/comisiones/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)
        
        return render_template(self.template, evento=evento)
                
    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
            id_cuenta = request.form.get('eliminar')
            cuenta = Cuenta[id_cuenta]
            evento.st_encargados.remove(cuenta)
            evento.st_colaboradores.remove(cuenta)
        except:
            abort(404)
        
        return redirect(f'/comisiones/{id_evento}')
    
route(pag_comisiones, Comision)


class AgregarCuenta(Controlador):
    template = 'comisiones/agregar.html'
    url = '/comisiones/<int:id_evento>/agregar'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormComisionAgregarCuenta()
        # obtenemos todas las cuentas para el autocompletado
        cuentas = orm.select(_ for _ in Cuenta).order_by(Cuenta.usuario)
        
        return render_template(self.template, evento=evento,
            form=form, cuentas=cuentas)

    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormComisionAgregarCuenta()
        if form.validate():
            # buscamos una cuenta que su nombre sea igual al del formulario
            cuenta_query = orm.select(cuent for cuent in Cuenta if cuent.usuario == form.cuenta.data)
            if len(cuenta_query) == 0:
                flash('No existe la cuenta.', 'error')
                return redirect(f'/comisiones/{id_evento}/agregar')

            cuenta = cuenta_query.first()
            if form.rol.data == 'encargado':
                evento.st_encargados.add(cuenta)
            else:
                evento.st_colaboradores.add(cuenta)
            
            flash(f'Cuenta "{ cuenta.usuario }" agregada.')
            return redirect(f'/comisiones/{id_evento}')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/comisiones/{id_evento}/crear')

route(pag_comisiones, AgregarCuenta)
