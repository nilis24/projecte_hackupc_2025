from extensions import db

# Taula Equip
class Equip(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codi = db.Column(db.String(10), unique=True)
    creador_nom = db.Column(db.String(100))
    membres = db.relationship('Membre', backref='equip', lazy=True)
    respostes = db.relationship('Resposta', backref='equip', lazy=True)

# Taula Membre
class Membre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100))
    equip_id = db.Column(db.Integer, db.ForeignKey('equip.id'), nullable=False)
    
    # Relació 1 a 1 amb Resposta
    resposta = db.relationship('Resposta', backref='membre', uselist=False)
    
# Taula Resposta
class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clima_preferit = db.Column(db.String(50))
    importancia_ecologia = db.Column(db.Integer)
    allotjament_preferit = db.Column(db.String(50))
    nivell_esport = db.Column(db.String(50))
    preferencia_transport = db.Column(db.String(50))
    ubicacio_actual = db.Column(db.String(100))
    pressupost_maxim = db.Column(db.Float)
    durada_viatge = db.Column(db.Integer)
    
    # Relacions
    prioritats = db.relationship('Prioritat', backref='resposta', lazy=True)
    interessos = db.relationship('Interes', backref='resposta', lazy=True)
    idiomes = db.relationship('Idioma', backref='resposta', lazy=True)
    restriccions = db.relationship('Restriccio', backref='resposta', lazy=True)

    # Clau forana que vincula la resposta amb l'equip
    equip_id = db.Column(db.Integer, db.ForeignKey('equip.id'), nullable=False)
    membre_id = db.Column(db.Integer, db.ForeignKey('membre.id'), nullable=False)
    
# Taula Prioritat
class Prioritat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria = db.Column(db.String(50))
    posicio = db.Column(db.Integer)
    
    # Clau forana que vincula la prioritat a una resposta
    resposta_id = db.Column(db.Integer, db.ForeignKey('resposta.id'), nullable=False)

# Taula Interes
class Interes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_interes = db.Column(db.String(100))
    
    # Clau forana que vincula l'interès a una resposta
    resposta_id = db.Column(db.Integer, db.ForeignKey('resposta.id'), nullable=False)

# Taula Idioma
class Idioma(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50))
    codi_iso = db.Column(db.String(5), unique=True)
    
    # Relació amb resposta
    resposta_id = db.Column(db.Integer, db.ForeignKey('resposta.id'), nullable=False)

# Taula Restriccio
class Restriccio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_restriccio = db.Column(db.String(100))
    
    # Clau forana que vincula la restricció a una resposta
    resposta_id = db.Column(db.Integer, db.ForeignKey('resposta.id'), nullable=False)

# Taula Lloc
class Lloc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iataCode = db.Column(db.String)
    nom = db.Column(db.String)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    vibes = db.Column(db.JSON)

