from flask import request
import random, string
import sqlite3

def crear_fitxa_de_pais(pais):
    pass


def crear_fitxa_conjunta_viatgers(fitxes_viatgers):
    pass


def crear_percentatges_coincidencia_per_pais(paisos, fitxa_viatger_conjunta):
    pass

def crear_equips():

    dades = request.get_json()
    if not dades or 'nomCreador' not in dades or 'nParticipants' not in dades or 'nomEquip' not in dades:
        return {"error": "Dades incorrectes o incompletes"}, 400
    codi_random = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    nom_creador = dades['nomCreador']
    n_participants = dades['nParticipants']
    
