from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Paquete, Inscrito, Comprobante, Egreso
from pony import orm
from app import *
from forms import FormCrearEgreso
from datetime import date
from decimal import Decimal
from uuid import uuid4

pag_caja = Blueprint('caja', __name__)

class Eventos(Controlador):
    template = 'caja/eventos.html'
    url = '/caja'

    def get(self):
        # mostrar todos los eventos con su caja
        return render_template(self.template,
                eventos=obtenerTodo(Evento, reverse=True))

route(pag_caja, Eventos)


class Ingresos(Controlador):
    template = 'caja/ingresos.html'
    url = '/caja/ingresos/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        return render_template(self.template, evento=evento)

route(pag_caja, Ingresos)


class Egresos(Controlador):
    template = 'caja/egresos.html'
    url = '/caja/egresos/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        return render_template(self.template, evento=evento)

route(pag_caja, Egresos)


class CrearEgreso(Controlador):
    template = 'caja/crear_egreso.html'
    url = '/caja/egresos/<int:id_evento>/crear'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormCrearEgreso()
        form.codigo.data = str(uuid4())
        return render_template(self.template, evento=evento, form=form)
                
    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormCrearEgreso()
        if form.validate():
            # en caso de que ya exista el codigo
            egreso = Egreso.get(pk_id=form.codigo.data)
            if egreso:
                flash('Código de comprobante ya registrado.', 'error')
                return redirect(f'/caja/egresos/{id_evento}/crear')

            # en caso de que el egreso sea mayor que lo que hay en la caja
            if evento.fk_caja.saldo < decimalToInt(form.monto.data):
                flash('Monto supera al saldo actual.', 'error')
                return redirect(f'/caja/egresos/{id_evento}/crear')

             # creamos el egreso y actualizamos el saldo de la caja    
            egreso = Egreso(
                pk_id=form.codigo.data,
                fk_caja=evento.fk_caja,
                descripcion=form.descripcion.data,
                fecha_emision=form.fecha_emision.data.isoformat(),
                monto=decimalToInt(form.monto.data))
            evento.fk_caja.saldo -= egreso.monto
            flash('Egreso creado exitosamente.')
            return redirect(f'/caja/egresos/{id_evento}')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/caja/egresos/{id_evento}/crear')

route(pag_caja, CrearEgreso)
