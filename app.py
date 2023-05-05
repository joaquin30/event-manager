from flask import Flask
from functools import wraps
from vistas import pags
from modelos import db
import os

# crear App

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_manager.db'
app.config['SECRET_KEY'] = os.urandom(20)
db.init_app(app)

with app.app_context():
    db.create_all()

# Configurar rutas

def route(Pag):
    view = Pag.as_view(Pag.__name__)
    app.add_url_rule(Pag.url, view_func=view)

for pag in pags:
    route(pag)

if __name__ == '__main__':
    app.run(debug=True)
