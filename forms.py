from flask_wtf import FlaskForm
from flask_wtf.file import *
from wtforms import *
from wtforms.validators import *
from datetime import date

def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024
    def file_length_check(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f"File size must be less than {max_size_in_mb}MB")
        field.data.seek(0)
    return file_length_check

class FormCrearEvento(FlaskForm):
    nombre = StringField('Nombre', [DataRequired(), Length(min=1, max=100)])
    descripcion = TextAreaField('Descripción', [DataRequired(), Length(min=1, max=1000)])
    img = FileField('Imagen del evento', [FileAllowed(['jpg', 'png', 'webp', 'bmp', 'gif', 'jpeg']),
        FileRequired(), FileSizeLimit(5)])
    submit = SubmitField('Crear evento')

class FormModificarEvento(FlaskForm):
    nombre = StringField('Nombre', [DataRequired(), Length(min=1, max=100)])
    descripcion = TextAreaField('Descripción', [DataRequired(), Length(min=1, max=1000)])
    img = FileField('Nueva imagen del evento', [Optional(),
        FileAllowed(['jpg', 'png', 'webp', 'bmp', 'gif', 'jpeg']), FileSizeLimit(5), ])
    submit = SubmitField('Modificar evento')

class FormCrearActividad(FlaskForm):
    nombre = StringField('Nombre', [DataRequired(), Length(min=1, max=100)])
    descripcion = TextAreaField('Descripción', [DataRequired(), Length(min=1, max=1000)])
    fecha_inicio = DateField('Fecha de inicio', [DataRequired()])
    fecha_fin = DateField('Fecha de fin', [DataRequired()])
    submit = SubmitField('Crear actividad')

class FormModificarActividad(FlaskForm):
    nombre = StringField('Nombre', [DataRequired(), Length(min=1, max=100)])
    descripcion = TextAreaField('Descripción', [DataRequired(), Length(min=1, max=1000)])
    fecha_inicio = DateField('Fecha de inicio', [DataRequired()])
    fecha_fin = DateField('Fecha de fin', [DataRequired()])
    submit = SubmitField('Modificar actividad')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MultiCheckboxAtLeastOne():
    def __init__(self, message=None):
        if not message:
            message = 'At least one option must be selected.'
        self.message = message

    def __call__(self, form, field):
        if len(field.data) == 0:
            raise StopValidation(self.message)

class FormCrearPaquete(FlaskForm):
    nombre = StringField('Nombre', [DataRequired(), Length(min=1, max=100)])
    precio = DecimalField('Precio', [DataRequired(), NumberRange(min=0)], step=0.10)
    actividades = MultiCheckboxField('Actividades', [MultiCheckboxAtLeastOne()], coerce=int)
    submit = SubmitField('Crear paquete')

class FormModificarPaquete(FlaskForm):
    nombre = StringField('Nombre', [DataRequired(), Length(min=1, max=100)])
    precio = DecimalField('Precio', [DataRequired(), NumberRange(min=0)], step=0.10)
    actividades = MultiCheckboxField('Actividades', [MultiCheckboxAtLeastOne()], coerce=int)
    submit = SubmitField('Modificar paquete')

class FormPreinscripcion(FlaskForm):
    doc_identidad = IntegerField('Documento de identidad', [DataRequired(), NumberRange(min=0)])
    nombre = StringField('Nombre', [Length(min=1, max=100), DataRequired()])
    telefono = StringField('Número telefónico', [Length(min=9, max=9), Regexp('^[0-9]*$'), DataRequired()])
    correo = StringField('Correo electrónico', [Length(max=100), Email(), DataRequired()])
    paquete = RadioField('Paquete', [DataRequired()])
    submit = SubmitField('Preinscribirse')

class FormCrearEgreso(FlaskForm):
    codigo = StringField('Código de comprobante', [DataRequired(), Length(max=40)])
    fecha_emision = DateField('Fecha', [DataRequired()])
    descripcion = StringField('Justificación', [DataRequired(), Length(max=100)])
    monto = DecimalField('Monto', [DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Crear egreso')
