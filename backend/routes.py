from flask import render_template
import random, string
from flask import render_template, redirect, url_for, session
from models import db, Equip, Membre
from flask_socketio import join_room, emit



def configure_routes():
    # crear equip (input nom equip)
    @app.route("/crear_equip", methods=["GET", "POST"])
    def crear_equip():
        if request.method == "POST":
            nom = request.form["nom"]
            codi = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            equip = Equip(creador_nom=nom, codi=codi)
            db.session.add(equip)
            db.session.commit()
            return redirect(url_for("sala_equip", codi=codi))
        return render_template("crear_equip.html")

    # pantalla sala equip
    @app.route("/equip/<codi>")
    def sala_equip(codi):
        equip = Equip.query.filter_by(codi=codi).first_or_404()
        return render_template("sala_equip.html", equip=equip)

    # unirse a un equip (input nom de membre i redireccio a formulari)
    @app.route("/unir/<codi>", methods=["GET", "POST"])
    def unir(codi):
        equip = Equip.query.filter_by(codi=codi).first_or_404()
        if request.method == "POST":
            nom = request.form["nom"]
            membre = Membre(nom=nom, equip_id=equip.id)
            db.session.add(membre)
            db.session.commit()

            # Notificació per WebSocket
            socketio.emit('nou_membre', {'nom': nom}, room=codi)

            session["membre_id"] = membre.id
            return redirect(url_for("formulari", membre_id=membre.id))
        return render_template("unir.html", equip=equip)

    # vista del formulari
    @app.route("/formulari/<int:membre_id>", methods=["GET", "POST"])
    def formulari(membre_id):
        membre = Membre.query.get_or_404(membre_id)
        if request.method == "POST":
            respostes = request.form.to_dict()
            membre.respostes = respostes
            db.session.commit()
            return redirect(url_for("gracies"))
        return render_template("formulari.html", membre=membre)

    @app.route("/espera")
    def espera():
        return render_template('espera.html')

    @app.route("/")
    def index():
        return render_template('index.html')
    
    @app.route("/resultats/<codi>")
    def resultats(codi):
        # Aquí carregaries les dades reals
        return render_template("resultats.html", codi=codi)
    


def configure_sockets(socketio):
    @socketio.on("join")
    def handle_join(data):
        room = data["room"]
        join_room(room)
        emit("nou_membre", {"nom": data["nom"]}, to=room)

    @socketio.on("processar_resultats")
    def processar(data):
        room = data["room"]
        # Aquí pots fer el processament que calgui abans d'enviar
        emit("resultats_preparats", {}, to=room)

    @socketio.on("formulari_completat")
    def on_formulari_completat(data):
        emit('formulari_completat', data, room=data['codi_equip'])
