from flask import render_template, redirect, flash, abort, Blueprint, request
from models import Cuenta, Caja
from pony import orm
from app import *
from forms import FormCrearCuenta
from datetime import date
from flask_simplelogin import login_required

pag_cuentas = Blueprint('cuentas', __name__)

# Pagina de todos los cuenta
class Cuentas(Controlador):
    decorators = [login_required(must=[es_superusuario])]
    url = '/cuentas'
    template = 'cuentas/cuentas.html'
    
    def get(self):
        return render_template(self.template, # seleccionamos todas las cuentas menos el admin
                cuentas=orm.select(cuenta for cuenta in Cuenta if cuenta.usuario != 'admin').order_by(Cuenta.usuario))

    def post(self):
        id_cuenta = request.form.get('eliminar')
        if not id_cuenta: # cambiamos el estado de superusuario
            id_cuenta = request.form.get('superusuario')
            print(Cuenta[id_cuenta].superusuario)
            Cuenta[id_cuenta].superusuario = not Cuenta[id_cuenta].superusuario
        else: # eliminamos la cuenta
            Cuenta[id_cuenta].delete()
            
        return redirect(self.url)

route(pag_cuentas, Cuentas)


class CrearCuenta(Controlador):
    decorators = [login_required(must=[es_superusuario])]
    url = '/cuentas/crear'
    template = 'cuentas/crear.html'

    def get(self):
        form = FormCrearCuenta()
        return render_template(self.template, url=self.url, form=form)

    def post(self):
        form = FormCrearCuenta()
        if form.validate():
            # si existe ya una cuenta con ese nombre
            if len(orm.select(cuenta for cuenta in Cuenta if cuenta.usuario == form.usuario.data)) > 0:
                flash('El nombre de usuario ya existe.', 'error')
                return redirect('/cuentas/crear')
                
            # creamos la cuenta
            cuenta = Cuenta(usuario=form.usuario.data,
                    contrasenha=form.contrasenha.data,
                    superusuario=False)

            return redirect('/cuentas')
        else:
            flash('Errores en el formulario.', 'error')
            return redirect('/cuentas/crear')

route(pag_cuentas, CrearCuenta)

