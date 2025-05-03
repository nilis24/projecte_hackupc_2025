from flask import SQLAlchemy
from models import Equip, Participant

def crear_equip(nom_creador: str, n_participants: int, codi: str):
    nou_equip = Equip(codi=codi, creador_nom=creador_nom)
    db.session.add(nou_equip)
    db.session.commit()

    return {"message": "Equip creat correctament", "equip_id": nou_equip.id}, 201
