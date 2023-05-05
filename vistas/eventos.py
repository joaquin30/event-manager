from vistas import Vista
from controladores import gestor_eventos 
from flask import render_template, redirect, request

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

class PagCrearEvento(Vista):
    """Página donde se crea un evento. Tiene un formulario para
    cada elemento de un evento."""
    rol_minimo = 3
    url = '/eventos/crear'
    template = 'crear_evento.html'

    def mostrar(self):
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            desc = request.form.get('desc')
            fecha = request.form.get('fecha')
            id = gestor_eventos.crearEvento(nombre, fecha, desc)
            if id >= 0:
                img = request.files['img']
                img.save(f'static/{id}.png')
            return redirect(PagEventos.url)
        return render_template(self.template, url=self.url)


class PagModificarEvento(Vista):
    """Página donde se modifica un evento. Tiene un formulario para
    cada elemento de un evento."""
    rol_minimo = 3
    url = '/eventos/modificar/<int:id>'
    template = 'modificar_evento.html'

    def mostrar(self, id):
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            desc = request.form.get('desc')
            fecha = request.form.get('fecha')
            gestor_eventos.modificarEvento(id, nombre, fecha, desc)
            if not request.files.get('img'):
                img = request.files['img']
                img.save(f'static/{id}')
            return redirect(PagEventos.url)
        return render_template(self.template,
                evento=gestor_eventos.obtenerEvento(id),
                url=f'/eventos/modificar/{id}')

