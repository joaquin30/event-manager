from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Paquete, Inscrito, Comprobante, Egreso
from pony import orm
from app import Controlador, route, obtenerTodo
from forms import FormCrearEgreso
from datetime import date
from decimal import Decimal
from uuid import uuid4

pag_caja = Blueprint('caja', __name__)

class Eventos(Controlador):
    template = 'caja/eventos.html'
    url = '/caja'

    def get(self):
        return render_template(self.template,
                eventos=obtenerTodo(Evento, reverse=True))

route(pag_caja, Eventos)


class Ingresos(Controlador):
    template = 'caja/ingresos.html'
    url = '/ingresos/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        return render_template(self.template, evento=evento)

route(pag_caja, Ingresos)


class Egresos(Controlador):
    template = 'caja/egresos.html'
    url = '/egresos/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        return render_template(self.template, evento=evento)

route(pag_caja, Egresos)


class CrearEgreso(Controlador):
    template = 'caja/crear_egreso.html'
    url = '/egresos/<int:id_evento>/crear'

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
            egreso = Egreso.get(pk_id=form.codigo.data)
            if egreso is not None:
                flash('Código de comprobante ya registrado.', 'error')
                return redirect(f'/egresos/{id_evento}/crear')
                
            if evento.fk_caja.saldo - form.monto.data < Decimal(0):
                flash('Monto supera al saldo actual.', 'error')
                return redirect(f'/egresos/{id_evento}/crear')
                
            egreso = Egreso(
                pk_id=form.codigo.data,
                fk_caja=evento.fk_caja,
                descripcion=form.descripcion.data,
                fecha_emision=form.fecha_emision.data,
                monto=form.monto.data)
            evento.fk_caja.saldo -= egreso.monto
            orm.commit()
            flash('Egreso creado exitosamente.')
            return redirect(f'/egresos/{id_evento}')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/egresos/{id_evento}/crear')

route(pag_caja, CrearEgreso)
