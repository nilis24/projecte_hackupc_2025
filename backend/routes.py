from flask import render_template, redirect, url_for, session, request
import random, string
from models import Equip, Membre, Prioritat, Interes, Idioma, Restriccio, Resposta
from flask_socketio import join_room, emit, SocketIO
from utilitats import aeroports_propers
from extensions import db

def configure_routes(app, socketio):
    # crear equip (input nom equip)
    @app.route("/crear_equip", methods=["GET", "POST"])
    def crear_equip():
        if request.method == "POST":
            nom = request.form["nom"]
            codi = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
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
    @app.route("/unir", methods=["GET", "POST"])
    def unir():
        if request.method == "POST":
            codi = request.form["codi"]
            equip = Equip.query.filter_by(codi=codi).first_or_404()
            nom = request.form["nom"]
            membre = Membre(nom=nom, equip_id=equip.id)
            db.session.add(membre)
            db.session.commit()

            session["membre_id"] = membre.id
            return redirect(url_for("formulari", membre_id=membre.id))
        else: 
            codi = request.args.get("codi")
            equip = Equip.query.filter_by(codi=codi).first_or_404()
            return render_template("unir.html", equip=equip, codi=codi)

    # vista del formulari
    @app.route("/formulari/<int:membre_id>", methods=["GET", "POST"])
    def formulari(membre_id):
        membre = Membre.query.get_or_404(membre_id)
        if request.method == "POST":
            respostes = request.form.to_dict()

            # Processar les prioritats
            prioritat_ordre = respostes.get("prioritats_ordre", "")
            if prioritat_ordre:
                prioritat_ordre = prioritat_ordre.split(",")
                for posicio, categoria in enumerate(prioritat_ordre, start=1):
                    prioritat = Prioritat(categoria=categoria, posicio=posicio, resposta_id=membre.id)
                    db.session.add(prioritat)

            # Processar interessos
            interessos = request.form.getlist("interessos[]")
            for interes in interessos:
                nou_interes = Interes(nom_interes=interes, resposta_id=membre.id)
                db.session.add(nou_interes)

            # Processar idiomes
            idiomes = respostes.get("idiomes", "").split(",")
            for idioma in idiomes:
                nou_idioma = Idioma(nom=idioma.strip(), resposta_id=membre.id)
                db.session.add(nou_idioma)

            # Processar restriccions
            restriccions = request.form.getlist("restriccions_alimentaries[]")
            for restriccio in restriccions:
                nova_restriccio = Restriccio(nom_restriccio=restriccio, resposta_id=membre.id)
                db.session.add(nova_restriccio)

            # Guardar altres respostes
            resposta = Resposta(
                data_inici=respostes.get("data_inici"),
                data_fi=respostes.get("data_fi"),
                clima_preferit=respostes.get("clima"),
                importancia_ecologia=respostes.get("green_travel"),
                allotjament_preferit=respostes.get("allotjament"),
                nivell_esport=respostes.get("activitat_fisica"),
                preferencia_transport=respostes.get("transport"),
                ubicacio_actual=respostes.get("ubicacio"),
                pressupost_maxim=respostes.get("pressupost"),
                durada_viatge=respostes.get("durada"),
                equip_id=membre.equip_id,
                membre_id=membre.id  
            )
            db.session.add(resposta)
            db.session.commit()

            # Notificar que el membre ha completat el formulari
            socketio.emit('membre_completat', {'nom': membre.nom}, room=membre.equip.codi)

            return redirect(url_for("gracies", codi=membre.equip.codi))
        else:
            membre_id = membre.id
            nom = membre.nom
            codi = membre.equip.codi
            socketio.emit('nou_membre', {'nom': nom}, room=codi)
        return render_template("formulari.html", membre=membre, membre_id=membre_id)

    @app.route("/gracies")
    def gracies():
        membre_id = session.get("membre_id")
        if membre_id:
            membre = Membre.query.get(membre_id)
            if membre:
                socketio.emit("rejoin", {"room": membre.equip.codi, "nom": membre.nom}, room=membre.equip.codi)
                return render_template("gracies.html", nom=membre.nom, codi=membre.equip.codi)
        return redirect(url_for("index"))

    @app.route("/espera")
    def espera():
        return render_template('espera.html')

    @app.route("/")
    def index():
        return render_template('index.html')
    
    @app.route("/destinacions/<codi>")
    def resultats(codi):
        destinacions = processar_resultats(codi)
        return render_template("destinacions.html", codi=codi, destinacions=destinacions)

    @app.route("/aeroports-propers")
    def aeroports_mes_propers():
        # Sanitize and validate the response before returning
        aeroports = aeroports_propers()
        if not isinstance(aeroports, (list, dict)):
            return {"error": "Invalid data format"}, 400
            
        # Escape any HTML in the response
        if isinstance(aeroports, list):
            sanitized = [{k: escape(str(v)) for k,v in item.items()} for item in aeroports]
        else:
            sanitized = {k: escape(str(v)) for k,v in aeroports.items()}
            
        # Return JSON response with content-type header to prevent XSS
        return jsonify(sanitized), 200, {'Content-Type': 'application/json'}

    
    @app.route("/vols/<iataCodeDestinacio>/<data>") # data en format YYYY-MM-DD
    def vols_aeroport_destinacio(iataCodeDestinacio, data):
        nom_destinacio = Lloc.query.filter_by(iataCode=iataCodeDestinacio).first()
        aeroports_propers = aeroports_propers()
        year, month, day = data.split("-")
        vols = busqueda_live_vols(aeroports_mes_propers[0]["iataCode"], iataCodeDestinacio, year, month, day)
        return render_template("vols.html", vols=vols, nom_destinacio=aeroports_mes_propers[0]["name"], nom_origen=nom_origen.nom)
    
    @app.route('/api/actualitzacio/<codi>', methods=['GET', 'POST'])
    def verificar_actualitzacio(codi):
        equip = Equip.query.filter_by(codi=codi).first()
        if request.method == 'POST':
            if equip:
                equip.estat = 1
                db.session.commit()
                return {"success": True}, 200
            return {"error": "Equip no trobat"}, 404
        elif request.method == 'GET':
            if equip:
                return {"estat": equip.estat}, 200
            return {"error": "Equip no trobat"}, 404


def configure_sockets(socketio):
    @socketio.on("join")
    def handle_join(data):
        room = data["room"]
        equip = Equip.query.filter_by(codi=room).first()
        if not equip:
            return  # Si el codi no és vàlid, no fem res
        join_room(room)
        if "nom" in data and data["nom"]:
            emit("nou_membre", {"nom": data["nom"]}, to=room)
        else:
            emit("nou_membre", {"nom": "Amfitrio"}, to=room)

    @socketio.on("processar_resultats")
    def processar(data):
        room = data["room"]
        equip = Equip.query.filter_by(codi=room).first()
        if not equip:
            return  # Si el codi no és vàlid, no fem res
        print(f"Rebent esdeveniment processar_resultats per a la sala: {room}")
        equip = Equip.query.filter_by(codi=room).first()
        if equip:
            equip.actualitzat = True
            db.session.commit()
        emit("resultats_preparats", {}, to=room)
        print(f"Esdeveniment resultats_preparats emès a la sala: {room}")

    @socketio.on("formulari_completat")
    def on_formulari_completat(data):
        emit('formulari_completat', data, room=data['codi_equip'])
