from flask import render_template, redirect, flash, abort, Blueprint, request, send_file
from models import *
from pony import orm
from app import *
from forms import FormReporte
from datetime import date
from openpyxl import Workbook

pag_reportes = Blueprint('reportes', __name__)

class Eventos(Controlador):
    template = 'reportes/eventos.html'
    url = '/reportes'

    def get(self):
        return render_template(self.template,
                eventos=obtenerTodo(Evento, reverse=True))

route(pag_reportes, Eventos)


class GenerarReporte(Controlador):
    template = 'reportes/reportes.html'
    url = '/reportes/<int:id_evento>'
    filename = 'static/reporte.xlsx'

    def get(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)
        form = FormReporte()
        form.fecha_inicio.data = date.today()
        form.fecha_fin.data = date.today()
        # ~ form.modulos.choices = self.choices
        return render_template(self.template, evento=evento, form=form)
                
    def post(self, id_evento):
        try:
            evento = Evento[id_evento]
        except:
            abort(404)

        form = FormReporte()
        if form.validate():
            # guardamos las fechas de inicio y fin en str
            fecha_inicio = form.fecha_inicio.data.isoformat()
            fecha_fin = form.fecha_fin.data.isoformat()
            modulos = form.modulos.data

            # funcion pequeña para transformar una lista de Modelos en una lista de dicts
            toDict = lambda modelos: list(map(lambda x: x.to_dict(), modelos))

            # creamos el libro en excel
            book = Workbook()

            if 'ingresos' in modulos:
                ingresos = orm.select(ingreso for ingreso in evento.fk_caja.st_comprobantes \
                    if fecha_inicio <= ingreso.fecha_emision and ingreso.fecha_emision <= fecha_fin) \
                        .order_by(Comprobante.fecha_emision)[:]
                addSheet(book, 'Ingresos', toDict(ingresos))
                    
            if 'egresos' in modulos:
                egresos = orm.select(egreso for egreso in evento.fk_caja.st_egresos \
                    if fecha_inicio <= egreso.fecha_emision and egreso.fecha_emision <= fecha_fin) \
                        .order_by(Egreso.fecha_emision)[:]
                addSheet(book, 'Egresos', toDict(egresos))
            
            if 'preinscritos' in modulos:
                preinscritos = []
                for paq in evento.st_paquetes:
                    preinscritos += orm.select(preinscrito for preinscrito in paq.st_preinscritos) \
                        .order_by(Inscrito.nombre)[:]
                addSheet(book, 'Preinscritos', toDict(preinscritos))

            if 'inscritos' in modulos:
                inscritos = []
                for paq in evento.st_paquetes:
                    inscritos += orm.select(inscrito for inscrito in paq.st_inscritos) \
                        .order_by(Inscrito.nombre)[:]
                addSheet(book, 'Inscritos', toDict(inscritos))

            if 'materiales' in modulos:
                materiales = []
                for act in evento.st_actividades:
                    materiales += orm.select(material for material in act.st_materiales) \
                        .order_by(Material.nombre)[:]
                addSheet(book, 'Materiales', toDict(materiales))
                
            if 'asistencia' in modulos:
                inscritos = []
                for paq in evento.st_paquetes:
                    inscritos += orm.select(inscrito for inscrito in paq.st_inscritos) \
                        .order_by(Inscrito.nombre)[:]
                asistencia = []
                for inscrito in inscritos:
                    data = {'doc_identidad': inscrito.pk_id}
                    for act in evento.st_actividades:
                        data[act.nombre] = 'si' if inscrito in act.st_asistentes else 'no'
                    asistencia.append(data)
                addSheet(book, 'Asistencia', asistencia)

            # eliminamos la hoja por defector y guardamos el reportes
            del book['Sheet']
            book.save(self.filename)
            return send_file(self.filename,
                download_name=f'reporte_{fecha_inicio}_{fecha_fin}.xlsx')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect(f'/reportes/{id_evento}')
    
route(pag_reportes, GenerarReporte)

