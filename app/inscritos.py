from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Evento, Paquete, Inscrito, Comprobante
from pony import orm
from app import Controlador, route, obtenerTodo
from forms import FormCrearPaquete, FormModificarPaquete
from uuid import uuid4
from datetime import date
import qrcode

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
    url = '/inscritos/preinscritos/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        num_preinscritos = 0
        for paquete in evento.st_paquetes:
            num_preinscritos += paquete.st_preinscritos.count()
            
        return render_template(self.template, evento=evento, num_preinscritos=num_preinscritos)
                
    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
            id_inscrito, id_paquete = request.form.get('inscribir').split()
            inscrito = Inscrito[id_inscrito]
            paquete = Paquete[id_paquete]
        except:
            abort(404)

        # movemos del grupo de preinscritos a los inscritos
        paquete.st_preinscritos.remove(inscrito)
        paquete.st_inscritos.add(inscrito)

        # generamos su codigo qr
        qr = qrcode.make(inscrito.get_pk())
        qr.save(f'static/qr/{inscrito.get_pk()}.png')

        # generamos el comprobante
        comprobante = Comprobante(
            pk_id=str(uuid4()),
            fk_caja=evento.fk_caja,
            fk_inscrito=inscrito,
            descripcion=f'Compra de paquete {paquete.nombre} del evento {evento.nombre}',
            fecha_emision=date.today().isoformat(),
            monto=paquete.precio)
        evento.fk_caja.saldo += comprobante.monto
        return redirect(f'/inscritos/preinscritos/{id_evento}?id={inscrito.pk_id}')

route(pag_inscritos, Preinscritos)


class Inscritos(Controlador):
    template = 'inscritos/inscritos.html'
    url = '/inscritos/<int:id_evento>'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        # obtenemos el numero total de inscritos
        num_inscritos = 0
        for paquete in evento.st_paquetes:
            num_inscritos += paquete.st_inscritos.count()
        
        return render_template(self.template, evento=evento, num_inscritos=num_inscritos)

route(pag_inscritos, Inscritos)

