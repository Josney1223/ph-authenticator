from requests import post
from json import dumps

API_ENDPOINT_EMAIL: str = "http://10.147.17.25:2002/api/v1/GerarEmail/EmailBasico"

def create_email(to: list, title: str, body: str, copy: list[str] = [], ocult_copy: list[str] = []) -> dict:
    dict_email: dict = {}
    body_email: dict = {}

    dict_email["Destinatario"] = to
    dict_email["Cc"] = copy
    dict_email["Cco"] = ocult_copy
    dict_email["Assunto"] = title
    dict_email["Corpo"] = []
    
    body_email["Tipo"] = "texto"
    body_email["Conteudo"] = body

    dict_email["Corpo"].append(body_email)

    return dict_email

def send_email(dict_email: dict) -> bool:
    
    response = post(API_ENDPOINT_EMAIL, files={'file': ('body.json', dumps(dict_email).encode('utf-8'))})

    if response.status_code == 200:
        return True
    else:
        return False