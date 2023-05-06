from vistas import Vista#, FileSizeLimit
from controladores import gestor_eventos 
from flask import render_template, redirect, request, flash 
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField, DateField
from wtforms.validators import Length, DataRequired, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import ValidationError
from datetime import date

def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024
    def file_length_check(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f"File size must be less than {max_size_in_mb}MB")
        field.data.seek(0)
    return file_length_check

class PagEventos(Vista):
    """Página donde se crea, modifica
    o elimina eventos, solo accesible al administrador.
    """
    rol_minimo = 3
    template = 'eventos.html'
    url = '/eventos'
    
    def mostrar(self):
        if request.method == 'POST':
            id = request.form.get('eliminar')
            gestor_eventos.eliminarEvento(id)
            return redirect(self.url)
        return render_template(self.template,
                eventos=gestor_eventos.obtenerEventos())

class FormEvento(FlaskForm):
    nombre = StringField('Nombre', [Length(min=1, max=100), DataRequired()])
    fecha = DateField('Fecha', [DataRequired()])
    desc = TextAreaField('Descripción', [Length(min=1, max=1000), DataRequired()])
    img = FileField('Imagen del evento', [FileAllowed(['jpg', 'png', 'webp', 'bmp', 'gif', 'jpeg']),
        FileRequired(), FileSizeLimit(5)])

class FormModificarEvento(FlaskForm):
    nombre = StringField('Nombre', [Length(min=1, max=100), DataRequired()])
    fecha = DateField('Fecha', [DataRequired()])
    desc = TextAreaField('Descripción', [Length(min=1, max=1000), DataRequired()])
    img = FileField('Imagen del evento', [Optional(),
        FileAllowed(['jpg', 'png', 'webp', 'bmp', 'gif', 'jpeg']), FileSizeLimit(5), ])

class PagCrearEvento(Vista):
    """Página donde se crea un evento. Tiene un formulario para
    cada elemento de un evento."""
    rol_minimo = 3
    url = '/eventos/crear'
    template = 'crear_evento.html'

    def mostrar(self):
        form = FormEvento()
        if form.validate_on_submit():
            nombre = form.nombre.data
            fecha = form.fecha.data
            desc = form.desc.data
            id = gestor_eventos.crearEvento(nombre, fecha, desc)
            if id >= 0:
                img = form.img.data
                img.save(f'static/{id}.png')
            return redirect(PagEventos.url)
        return render_template(self.template, url=self.url, form=form)


class PagModificarEvento(Vista):
    """Página donde se modifica un evento. Tiene un formulario para
    cada elemento de un evento."""
    rol_minimo = 3
    url = '/eventos/modificar/<int:id>'
    template = 'modificar_evento.html'

    def mostrar(self, id: int):
        form = FormModificarEvento()
        if form.validate_on_submit():
            nombre = form.nombre.data
            fecha = form.fecha.data
            desc = form.desc.data
            gestor_eventos.modificarEvento(id, nombre, fecha, desc)
            if form.img.data is not None:
                img = form.img.data
                img.save(f'static/{id}.png')
            return redirect(PagEventos.url)
        evento = gestor_eventos.obtenerEvento(id)
        form.nombre.data = evento.nombre
        form.fecha.data = date.fromisoformat(evento.fecha)
        form.desc.data = evento.descripcion
        return render_template(self.template, url=f'/eventos/modificar/{id}', form=form,
                evento=evento)

