from flask import Flask, render_template, request, redirect, url_for, session
import random, string
from flask_socketio import SocketIO
from routes import configure_routes, configure_sockets
from models import db, Equip, Membre

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Inicialitzar la base de dades
with app.app_context():
    db.init_app(app)
    db.create_all()

# Registrem les rutes i els sockets en l'app
configure_routes(app)
configure_sockets(socketio)

if __name__ == "__main__":
    socketio.run(app, debug=True)
