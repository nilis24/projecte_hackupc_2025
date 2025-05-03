from flask import request
import random, string
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func
from models import app, Resposta, Equip, Prioritat
from collections import Counter
import difflib
import json

db = SQLAlchemy(app)


def calcula_mode(llista):
    if not llista:
        return []

    contador = Counter(llista)
    max_freq = max(contador.values())
    modes = [element for element, freq in contador.items() if freq == max_freq]
    return modes



def calcular_prioritats_mitjanes(equip_id):
    resultats = (
        db.session.query(
            Prioritat.categoria,
            func.avg(Prioritat.posicio).label("mitjana_posicio")
        )
        .join(Resposta, Prioritat.resposta_id == Resposta.id)
        .filter(Resposta.equip_id == equip_id)
        .group_by(Prioritat.categoria)
        .order_by(func.avg(Prioritat.posicio).asc())
        .all()
    )
    return resultats



def crear_fitxa_de_pais(pais):
    pass


def crear_fitxa_conjunta_viatgers(codi_equip):
    respostes = Resposta.query.filter_by(equip_id=equip.id).all()
    # clima
    climes = [r.clima_preferit for r in respostes]
    clima_comu = calcula_mode(climes)
    # Processar pressupost
    pressupostos = [r.pressupost_maxim for r in respostes]
    pressupost_mig = sum(pressupostos) / len(pressupostos)

    # Processar preferencia de transport
    preferencies_transport = [r.preferencia_transport for r in respostes]
    preferencia_transport_comu = calcula_mode(preferencies_transport)

    # Processar nivell d'esport
    nivells_esport = [r.nivell_esport for r in respostes]
    nivell_esport_comu = calcula_mode(nivells_esport)

    # Processar importancia de l'ecologia
    importancies_ecologia = [r.importancia_ecologia for r in respostes]
    importancia_ecologia_comu = calcula_mode(importancies_ecologia)

    # Processar preferencia d'allotjament
    preferencies_allotjament = [r.allotjament_preferit for r in respostes]
    preferencia_allotjament_comu = calcula_mode(preferencies_allotjament)

    # Processar durada del viatge
    durades_viatge = [r.durada_viatge for r in respostes]
    durada_viatge_mig = sum(durades_viatge) / len(durades_viatge)

    # Processar idiomes
    idiomes = [r.idioma for r in respostes]
    idiomes_comuns = list(set(idiomes))

    # Processar interessos
    interessos = [r.interes for r in respostes]
    interessos_comuns = list(set(interessos))

    # Processar restriccions
    restriccions = [r.restriccio for r in respostes]
    restriccions_comunes = list(set(restriccions))

    # processar prioritats

    # Crear fitxa conjunta
    fitxa_conjunta = {
        "clima": clima_comu,
        "pressupost": pressupost_mig,
        "preferencia_transport": preferencia_transport_comu,
        "nivell_esport": nivell_esport_comu,
        "importancia_ecologia": importancia_ecologia_comu,
        "allotjament_preferit": preferencia_allotjament_comu,
        "durada_viatge": durada_viatge_mig,
        "idiomes": idiomes_comuns,
        "interessos": interessos_comuns,
        "restriccions": restriccions_comunes,   
        "prioritats": calcular_prioritats_mitjanes(equip_id),
    }

    return fitxa_conjunta



def normalitza_valor(valor):
    if isinstance(valor, str):
        return valor.strip().lower()
    if isinstance(valor, list):
        return sorted([normalitza_valor(x) for x in valor])
    if isinstance(valor, dict):
        return {k.lower(): normalitza_valor(v) for k, v in valor.items()}
    return valor


def compara_valors(v1, v2):
    v1 = normalitza_valor(v1)
    v2 = normalitza_valor(v2)
    
    if isinstance(v1, str) and isinstance(v2, str):
        return difflib.SequenceMatcher(None, v1, v2).ratio()
    if isinstance(v1, list) and isinstance(v2, list):
        comuns = set(v1) & set(v2)
        total = set(v1) | set(v2)
        if not total:
            return 1.0
        return len(comuns) / len(total)
    if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
        rang = max(abs(v1), abs(v2), 1)
        return 1.0 - abs(v1 - v2) / rang
    if isinstance(v1, dict) and isinstance(v2, dict):
        return compara_dicts(v1, v2)
    return 0.0


def compara_dicts(d1, d2):
    claus_comunes = set(d1.keys()) & set(d2.keys())
    if not claus_comunes:
        return 0.0
    similituds = [compara_valors(d1[k], d2[k]) for k in claus_comunes]
    return sum(similituds) / len(similituds)


def calcula_coincidencia(fitxa1: dict, fitxa2: dict) -> float:
    fitxa1 = normalitza_valor(fitxa1)
    fitxa2 = normalitza_valor(fitxa2)
    return compara_dicts(fitxa1, fitxa2)



def processar_resultats(codi_equip):
    resultats = {}
    paisos = Pais.query.all()
    fitxa_conjunta = crear_fitxa_conjunta_viatgers(codi_equip)
    for pais in paisos:
        fitxa_pais = crear_fitxa_de_pais(pais)
        coincidencia = calcula_coincidencia(fitxa_conjunta, fitxa_pais)
        resultats[pais.nom] = coincidencia
    top_three = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True)[:3])
    return top_three
        



def crear_equips():

    dades = request.get_json()
    if not dades or 'nomCreador' not in dades or 'nParticipants' not in dades or 'nomEquip' not in dades:
        return {"error": "Dades incorrectes o incompletes"}, 400
    codi_random = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    nom_creador = dades['nomCreador']
    n_participants = dades['nParticipants']
    
