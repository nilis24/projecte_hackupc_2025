from flask import SQLAlchemy

def crear_equip(db: SQLAlchemy, dades: dict):
    codi = dades.get('codi')
    creador_nom = dades.get('creador_nom')

    if not codi or not creador_nom:
        return {"error": "Falten dades obligatòries"}, 400

    nou_equip = Equip(codi=codi, creador_nom=creador_nom)
    db.session.add(nou_equip)
    db.session.commit()

    return {"message": "Equip creat correctament", "equip_id": nou_equip.id}, 201
