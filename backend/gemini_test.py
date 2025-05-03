import requests

def aeroports_mes_propers():
    ip = request.remote_addr
    url = "https://exemple.com/api"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": ""
    }
    body = {
        "locator": {
            "ipAddress": "147.83.201.131"
        },
        "locale": "en-GB"
    }