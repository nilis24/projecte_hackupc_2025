from flask import Flask, render_template, request, redirect, url_for, session
import random, string, secrets
from flask_socketio import SocketIO
from extensions import db

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Initialize SQLAlchemy with the app
db.init_app(app)

# Import routes after db initialization to avoid circular imports
from routes import configure_routes, configure_sockets
from models import Equip, Membre

# Create all database tables
with app.app_context():
    db.create_all()

# Registrem les rutes i els sockets en l'app
configure_routes(app, socketio)
configure_sockets(socketio)

if __name__ == "__main__":
    socketio.run(app, debug=True)
