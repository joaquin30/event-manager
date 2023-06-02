from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Paquete, Inscrito, Comprobante
from pony import orm
from app import Controlador, route, obtenerTodo
from forms import FormCrearPaquete, FormModificarPaquete
from uuid import uuid4
from datetime import date

pag_inscritos = Blueprint('inscritos', __name__)

class Eventos(Controlador):
    template = 'inscritos/eventos.html'
    url = '/inscritos'

    def get(self):
        return render_template(self.template,
                eventos=obtenerTodo(Evento, reverse=True))

route(pag_inscritos, Eventos)


class Preinscritos(Controlador):
    template = 'inscritos/preinscritos.html'
    url = '/preinscritos/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        return render_template(self.template, evento=evento)
                
    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
            id_inscrito, id_paquete = request.form.get('inscribir').split()
            inscrito = Inscrito[id_inscrito]
            paquete = Paquete[id_paquete]
        except:
            abort(404)

        paquete.st_preinscritos.remove(inscrito)
        paquete.st_inscritos.add(inscrito)
        comprobante = Comprobante(
            pk_id=str(uuid4()),
            fk_caja=evento.fk_caja,
            fk_inscrito=inscrito,
            descripcion=f'Compra de paquete {paquete.nombre} del evento {evento.nombre}',
            fecha_emision=date.today(),
            monto=paquete.precio)
        evento.fk_caja.saldo += comprobante.monto
        orm.commit()
        return redirect(f'/preinscritos/{id_evento}')

route(pag_inscritos, Preinscritos)


class Inscritos(Controlador):
    template = 'inscritos/inscritos.html'
    url = '/inscritos/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        return render_template(self.template, evento=evento)

route(pag_inscritos, Inscritos)

