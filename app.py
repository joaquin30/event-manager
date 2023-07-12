from flask import Flask
from pony import orm
from pony.flask import Pony
from models import Cuenta
from flask_simplelogin import SimpleLogin, Message
import os
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20)
Pony(app)

# Añadimos todods los controladores a la app
from app.inicio import pag_inicio
app.register_blueprint(pag_inicio)
from app.ambientes import pag_ambientes
app.register_blueprint(pag_ambientes)
from app.eventos import pag_eventos
app.register_blueprint(pag_eventos)
from app.actividades import pag_actividades
app.register_blueprint(pag_actividades)
from app.paquetes import pag_paquetes
app.register_blueprint(pag_paquetes)
from app.inscritos import pag_inscritos
app.register_blueprint(pag_inscritos)
from app.caja import pag_caja
app.register_blueprint(pag_caja)
from app.colaborador import pag_colaborador
app.register_blueprint(pag_colaborador)
from app.cuentas import pag_cuentas
app.register_blueprint(pag_cuentas)
from app.comisiones import pag_comisiones
app.register_blueprint(pag_comisiones)
from app.reportes import pag_reportes
app.register_blueprint(pag_reportes)

# Creamos la cuenta admin
with orm.db_session:
    if len(orm.select(cuenta for cuenta in Cuenta if cuenta.usuario == 'admin')) == 0:
        admin = Cuenta(usuario='admin',
            contrasenha='admin', superusuario=True)
        orm.commit()

# Mensages para los distintos estados del login
messages = {
    'login_success': 'Inicio de sesión exitoso.',
    'login_failure': Message('Error en el inicio de sesión.', 'error'),
    'is_logged_in': 'Ya inició su sesión.',
    'logout': 'Cierre de sesión exitoso.',
    'login_required': Message('Necesita iniciar sesión.', 'error'),
    'access_denied': Message('Acceso denegado.', 'error'),
    'auth_error': Message('Error en la autenticación: {0}', 'error')
}

# iniciamos el modulo de login
def login_checker(user):
    query = orm.select(cuenta for cuenta in Cuenta if cuenta.usuario == user['username'])
    return len(query) > 0 and query.first().contrasenha == user['password']

SimpleLogin(app, messages=messages, login_checker=login_checker)

# Creamos un filtro para mostrar las fechas
@app.template_filter()
def format_date(value):
    res = ''
    try:
        res = date.fromisoformat(value).strftime('%d/%m/%y')
    except:
        res = 'Sin fecha'
    
    return res
    
# Creamos un filtro para mostrar el dinero
@app.template_filter()
def format_money(value):
    x = str(value // 100)
    y = value % 100
    if y < 10:
        y = '0' + str(y)
    return f'S/ {x}.{y}'

# Creamos un filtro para ver si el usuario es un superusuario
@app.template_filter()
def is_superuser(user):
    query = orm.select(cuenta for cuenta in Cuenta if cuenta.usuario == user)
    return len(query) > 0 and query.first().superusuario
    
if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
