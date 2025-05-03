from flask import Flask
from flask_socketio import SocketIO
from routes import configure_routes, configure_sockets

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Registrem les rutes i els sockets en l'app
configure_routes(app)
configure_sockets(socketio)

if __name__ == "__main__":
    socketio.run(app, debug=True)
