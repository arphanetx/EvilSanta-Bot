import os
import requests

BASE_URL = "https://gate.whapi.cloud"
TOKEN = os.environ.get("WHAPI_TOKEN", "yDvEPaO1kEI1dybAMRyZxCAHJgQLSqTz")
GROUP_ID = os.environ.get("WHAPI_GROUP_ID", "120363432518984499@g.us")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


def enviar_mensaje(to: str, text: str) -> dict:
    url = f"{BASE_URL}/messages/text"
    payload = {"to": to, "body": text}
    resp = requests.post(url, json=payload, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()


def enviar_al_grupo(text: str) -> dict:
    return enviar_mensaje(GROUP_ID, text)


def enviar_dm(to: str, text: str) -> dict:
    return enviar_mensaje(to, text)


def leer_mensajes(chat_id: str, limit: int = 20) -> list:
    url = f"{BASE_URL}/messages/list/{chat_id}"
    params = {"count": limit}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("messages", [])


def leer_mensajes_dm(numero: str, limit: int = 10) -> list:
    return leer_mensajes(numero, limit=limit)
