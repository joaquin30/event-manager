from flask import Flask
from flask_login import LoginManager, UserMixin
from functools import wraps
from vistas import *
from controladores import *
from modelos import *
import os

# crear App

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_manager.db'
app.config['SECRET_KEY'] = os.urandom(20)
db.init_app(app)

with app.app_context():
    db.create_all()

def populate_database():
    db.session.add(Evento(
        nombre='2do Congreso Latinoamericano de Publicidad',
        img='2pub.jpg',
        descripcion='Congreso de publicida en argentida, más de 150 disertantes',
        fecha='2018-03-06'))
    db.session.add(Evento(
        nombre='II Congreso Global de Investigadores',
        img='2invest.png',
        descripcion='Tema: Innovacion social para la paz',
        fecha='2016-11-09'))
    db.session.add(Evento(
        nombre='1er Congreso de Radiología',
        img='1rad.jpg',
        descripcion='Radiodiagnóstico en la práctica médica. ¡Lo que usted necesita saber!',
        fecha='2019-06-16'))
    db.session.commit()

# with app.app_context():
#     populate_database()
#     import sys
#     sys.exit()

# Configurar Login

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    id: int

@login_manager.user_loader
def user_loader(username):
    if not Usuario.query.exists().where(User.nombre == username).scalar():
        return
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if not Usuario.query.exists().where(User.nombre == username).scalar():
        return
    user = User()
    user.id = username
    return user

def login_required(view):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
              return login_manager.unauthorized()
            if current_user.rol < view.rol_minimo:
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


# Configurar rutas

def route(Pag):
    view = Pag.as_view(Pag.__name__)
    if Pag.rol_minimo > 0:
        view = login_required(view)
    app.add_url_rule(Pag.url, view_func=view)

route(PagInicio)
route(PagEvento)

if __name__ == '__main__':
    app.run(debug=True)
