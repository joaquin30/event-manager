from vistas import Vista
from controladores import gestor_eventos
from flask import render_template, redirect, request, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms.validators import Length, DataRequired, NumberRange, Regexp, Email
from datetime import date
from modelos import Tabla, Preinscrito

class FromPreinscripcion(FlaskForm):
    nombre = StringField('Nombre', [Length(min=1, max=100), DataRequired()])
    edad = IntegerField('Edad', [NumberRange(min=1, max=150), DataRequired()])
    telefono = StringField('Número telefónico', [Length(min=9, max=9), Regexp('^[0-9]*$'), DataRequired()])
    email = StringField('Correo electrónico', [Length(min=1, max=100), Email(), DataRequired()])

class PagPublicEvento(Vista):
    """Página web en la ruta `/evento/<int:evento_id>`.
    Muestra la descripción de un solo evento, además de tener
    el formulario para preinscribirse.
    """

    rol_minimo = 0
    template = 'public_evento.html'
    url = '/evento/<int:evento_id>'
     
    def mostrar(self, evento_id: int) -> str:
        form = FromPreinscripcion()
        if form.validate_on_submit():
            tabla = Tabla(Preinscrito)
            tabla.insertar(Preinscrito(
                nombre=form.nombre.data,
                edad=form.edad.data,
                telefono=form.telefono.data,
                email=form.email.data,
                evento_id=evento_id))
            return redirect('/')
        evento = gestor_eventos.obtenerEvento(evento_id)
        if evento is None:
            abort(404)
        return render_template(self.template,
                evento=evento, form=form)

