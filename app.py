from flask import Flask
from pony.flask import Pony
import os

app = Flask(__name__)
Pony(app)
app.config['SECRET_KEY'] = os.urandom(20)
from app.inicio import pag_inicio
app.register_blueprint(pag_inicio)
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

if __name__ == '__main__':
    app.run(debug=True)
