from flask import Flask
from pony.flask import Pony
from flask_simplelogin import SimpleLogin, Message
import os
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20)
Pony(app)

# Mensages para los distintos estados del login
messages = {
    'login_success': 'Inicio de sesión exitoso.',
    'login_failure': 'Error en el inicio de sesión.',
    'is_logged_in': 'Ya inició su sesión.',
    'logout': 'Cierre de sesión exitoso.',
    'login_required': Message('Necesita iniciar sesión.', 'error'),
    'access_denied': Message('Acceso denegado.', 'error'),
    'auth_error': Message('Error en la autenticación.', 'error')
}

SimpleLogin(app, messages=messages)

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
    
if __name__ == '__main__':
    app.run(debug=True)
