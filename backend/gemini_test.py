from google import genai
import json

client = genai.Client(api_key="AIzaSyC6YjQ-6TjwLFuiJYdBcKCNONnFD6Tb9ec")

nom_pais = "Suissa"

json_content = {
    "pais": "Nom del país",
    "capital": "Nom de la capital",
    
    "seguretat": {
        "nivell_general": "segur/moderat/perillós",
        "zones_a_evitar": ["", ""],
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

print(type(json.loads("\n".join(response.text.splitlines()[1:-1]))))
print(json.loads("\n".join(response.text.splitlines()[1:-1])))

