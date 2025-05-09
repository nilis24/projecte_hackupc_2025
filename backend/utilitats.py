from flask import request
import random, string
import sqlite3
from sqlalchemy import text, func
from models import Resposta, Equip, Prioritat
from collections import Counter
import difflib
import json
from google import genai
from main import db
from dotenv import load_dotenv
import requests
import os

load_dotenv()

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


def dades_guerres_paisos():
    url = "https://api.acleddata.com/acled/read/?key=suYecZD-kb-mIQYYparP&email=tawam99130@nutrv.com"
    response = requests.get(url)
    data = response.json()
    





def crear_fitxa_de_pais(pais):
    client = genai.Client(api_key=os.getenv("API_KEY_GENAI"))

    json_content = {
        "pais": "Nom del país",
        "capital": "Nom de la capital",
        
        "seguretat": {
            "nivell_general": "<enter: puntuatge -100-0, -100 és insegur i 0 és segur>",
            "alertes_actuals": ["", ""],
            "delictes_comuns": ["", ""]
        },
        
        "cultura_i_art": {
            "patrimoni_unesco": ["", "", ""],
            "festivals_culturals": [
                {
                    "nom": "",
                    "lloc": "",
                    "mes": "",
                    "tema": ""
                },
                {
                    "nom": "",
                    "lloc": "",
                    "mes": "",
                    "tema": ""
                }
            ],
            "arquitectura_emblematica": ["", "", ""],
            "museus_recomanats": ["", "", ""]
        },
        
        "musica_i_espectacles": {
            "estils_musicals_tipics": ["", ""],
            "artistes_famosos": ["", "", ""],
            "sales_concerts": ["", "", ""],
            "festivals_musicals": [
                {
                    "nom": "",
                    "ciutat": "",
                    "mes": ""
                }
            ]
        },
        
        "gastronomia": {
            "plats_tipics": ["", "", ""],
            "begudes_tipiques": ["", ""],
            "nivell_gastronomic": "alt/mitjà/baix",
            "mercats_gastronomics": ["", ""]
        },
        
        "economia_turistica": {
            "aportacio_pct_pib": 0.0,
            "turistes_anuals": 0,
            "temporada_alta": ["mes_inici", "mes_final"],
            "principals_motius_visita": ["platja", "cultura", "gastronomia"]
        },
        
        "atractius_principals": {
            "ciutats_populars": ["", "", ""],
            "platges_famoses": ["", ""],
            "parcs_nacionals": ["", ""],
            "turisme_rural": True,
            "turisme_aventura": True,
            "turisme_luxós": True
        },
        
        "transport_turistic": {
            "facilitat_mobilitat": "alta/mitjana/baixa",
            "targeta_turistica": True,
            "apps_utilitats": ["transport", "guies", "idiomes"],
            "idiomes_comunicacio": ["anglès", "idioma_local"]
        },
        
        "cost_viatge": {
            "pressupost_mitja_dia_usd": {
                "motxiller": 30,
                "estàndard": 80,
                "luxós": 200
            },
            "nivell_preus": "baix/mitjà/alt"
        },
        
        "comportaments_i_costums": {
            "propines": "opcional/inclosa/esperada",
            "normes_socials": ["saludar amb la mà", "puntualitat valorada"],
            "vestimenta": "informal/conservadora segons zona",
            "idioma_oficial": "",
            "altres_idiomes_comuns": ["anglès", ""]
        },
        
        "connectivitat": {
            "wifi_public": "freqüent/limitat/escàs",
            "sim_local_disponible": True,
            "velocitat_internet_mitjana_mbps": 0.0
        },
        
        "visa_i_entrada": {
            "necessita_visa": True,
            "tipus_visa": "a l'arribada/electrònica/previament",
            "dies_permesos": 0,
            "taxes_entrada_usd": 0
        }
    }


    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{json_content} \n\n Utilitza aquest esquema JSON com a plantilla per generar una fitxa tècnica detallada sobre el país {nom_pais}, amb informació turística rellevant i actualitzada. És important que matisis clarament l'estat de seguretat i estabilitat del país, indicant si és una destinació segura, si hi ha zones amb problemes, o si hi ha conflictes interns o externs que puguin afectar el turisme. Omple tots els camps amb dades completes, rigoroses i coherents amb la realitat actual. La resposta ha de consistir exclusivament en el JSON, sense cap explicació addicional.",
    )

    return json.loads("\n".join(response.text.splitlines()[1:-1]))

def aeroports_propers():
    ip = os.getenv("IP_PUBLICA_HACKUPC")
    url = "https://partners.api.skyscanner.net/apiservices/v3/geo/hierarchy/flights/nearest"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv("API_KEY_SKYSCANNER")
    }
    body = {
        "locator": {
            "ipAddress": ip
        },
        "locale": "en-GB"
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        aeroports = [
            {
                "name": data["name"],
                "iataCode": data["iata"]
            }
            for v in response["places"].values()
            if v.get("type") == "PLACE_TYPE_AIRPORT"
        ]
        return aeroports
    else:
        return {"error": "No s'ha pogut obtenir les dades de l'API"}

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

    # Processar data de viatge
    dates_viatge = [r.data_viatge for r in respostes]
    data_viatge_comu = calcula_mode(dates_viatge)[0]

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
        "data_viatge": data_viatge_comu,
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
    
    # Comprovar si el país està en la llista de països exclosos
    if 'paisos_exclosos' in fitxa1 and fitxa2.get('pais') in fitxa1['paisos_exclosos']:
        return 0.0
    
    return compara_dicts(fitxa1, fitxa2)



def enriquir_contingut_top_three(top_three):
    client = genai.Client(api_key=os.getenv("API_KEY_GENAI"))

    nova_estructura_json = [
        {
            "nom": "nom_pais_1",
            "coincidencia": 10.7,
            "descripcio": "<text de descripcio>",
            "caracteristiques": [
                {
                    "icona": "<icona de bootstrap icons>",
                    "text": "<text de la caracteristica>"
                },
                {
                    "icona": "<icona de bootstrap icons>",
                    "text": "<text de la caracteristica>"
                }
            ]
        },
        {
            "nom": "nom_pais_1",
            "coincidencia": 10.7,
            "descripcio": "<text de descripcio>",
            "caracteristiques": [
                {
                    "icona": "<icona de bootstrap icons>",
                    "text": "<text de la caracteristica>"
                },
                {
                    "icona": "<icona de bootstrap icons>",
                    "text": "<text de la caracteristica>"
                }
            ]
        }

    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{top_three} \n\n Donat aquest json, tradueixlo a la seguenta estructura json: {nova_estructura_json}. Enriqueixlo proporcionant contingut per cada país. Utilitza el teu conjunt de dades per a proporcionar informació detallada sobre cada país. Asegura't que les dades proporcionades siguin precises i actualitzades. La resposta ha de consistir exclusivament en el JSON, sense cap explicació addicional. IMPORTANT: no borris el camp de la data del viatge",
    )

    return json.loads("\n".join(response.text.splitlines()[1:-1]))




def processar_resultats(codi_equip):
    resultats = {}
    paisos = Pais.query.all()
    fitxa_conjunta = crear_fitxa_conjunta_viatgers(codi_equip)
    for pais in paisos:
        fitxa_pais = crear_fitxa_de_pais(pais)
        coincidencia = calcula_coincidencia(fitxa_conjunta, fitxa_pais)
        resultats[pais.nom] = coincidencia
    top_three = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True)[:3])
    top_three["data_viatge"] = fitxa_conjunta["data_viatge"]
    return enriquir_contingut_top_three(top_three)
        

def busqueda_live_vols(iataCodeOrigen, iataCodeDestinacio, any, mes, dia):
    data = {}
    poll_token = ""
    estat = ""
    # preparacio de la request /create
    url = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv("API_KEY_SKYSCANNER")
    }
    body = {
        "query": {
            "market": "UK",
            "locale": "en-GB",
            "currency": "EUR",
            "queryLegs": [
                {
                    "originPlaceId": {
                        "iata": iataCodeOrigen,
                    },
                    "destinationPlaceId": {
                        "iata": iataCodeDestinacio,
                    },
                    "date": {
                        "year": any,
                        "month": mes,
                        "day": dia
                    }
                }
            ],
        }
    }

    # execucio de la request /create
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        poll_token = data["sessionToken"]
        estat = data["status"]
    else:
        return {"error": "No s'ha pogut obtenir les dades de l'API"}

    
    i = 0
    while i < 3 and estat != "RESULT_STATUS_COMPLETE":
        # preparacio de la request /poll
        url = f"https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll/{poll_token}"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("API_KEY_SKYSCANNER")
        }
        # execucio de la request /poll
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            estat = data["status"]
            if estat != "RESULT_STATUS_COMPLETE":
                time.sleep(5)
            i+=1  
        else:
            return {"error": "No s'ha pogut obtenir les dades de l'API"}
            break
    else:
        if(estat != "RESULT_STATUS_COMPLETE"):
            return {"error": "No s'ha pogut obtenir les dades de l'API"}

    return data



def crear_equips():

    dades = request.get_json()
    if not dades or 'nomCreador' not in dades or 'nParticipants' not in dades or 'nomEquip' not in dades:
        return {"error": "Dades incorrectes o incompletes"}, 400
    codi_random = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    nom_creador = dades['nomCreador']
    n_participants = dades['nParticipants']
    
