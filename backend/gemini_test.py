import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def dades_guerres_paisos():
    url = f'https://api.acleddata.com/acled/read/?key={os.getenv("ACLEDATA_API_KEY")}&email={os.getenv("ACLEDATA_EMAIL")}'
    response = requests.get(url)
    data = response.json()
    response = requests.get(url)
    data = response.json()["data"]
    df = pd.DataFrame(data)

    # Fem el "GROUP BY"
    
    resultat = df.groupby(["sub_event_type", "country"]).agg(
        total_registres=('country', 'count')
    ).reset_index()
    
    return resultat 


print(dades_guerres_paisos())