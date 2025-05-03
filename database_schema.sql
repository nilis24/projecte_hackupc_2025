CREATE TABLE equip (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codi TEXT UNIQUE,
    creador_nom TEXT
);

CREATE TABLE membre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    equip_id INTEGER NOT NULL,
    FOREIGN KEY (equip_id) REFERENCES equip (id)
);

CREATE TABLE resposta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clima_preferit TEXT,
    importancia_ecologia INTEGER,
    allotjament_preferit TEXT,
    nivell_esport TEXT,
    preferencia_transport TEXT,
    ubicacio_actual TEXT,
    pressupost_maxim REAL,
    durada_viatge INTEGER,
    equip_id INTEGER NOT NULL,
    FOREIGN KEY (equip_id) REFERENCES equip (id)
);

CREATE TABLE prioritat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT,
    posicio INTEGER,
    resposta_id INTEGER NOT NULL,
    FOREIGN KEY (resposta_id) REFERENCES resposta (id)
);

CREATE TABLE interes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_interes TEXT,
    resposta_id INTEGER NOT NULL,
    FOREIGN KEY (resposta_id) REFERENCES resposta (id)
);

CREATE TABLE idioma (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    codi_iso TEXT UNIQUE,
    resposta_id INTEGER NOT NULL,
    FOREIGN KEY (resposta_id) REFERENCES resposta (id)
);

CREATE TABLE restriccio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_restriccio TEXT,
    resposta_id INTEGER NOT NULL,
    FOREIGN KEY (resposta_id) REFERENCES resposta (id)
);

CREATE TABLE pais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    codi_iso TEXT UNIQUE,
    continent_id INTEGER NOT NULL,
    FOREIGN KEY (continent_id) REFERENCES continent (id)
);

CREATE TABLE continent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT
);