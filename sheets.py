import csv
import io
import requests

SHEET_ID = "1sHMjUvyaUyp_a8f4HHx-oissAgBis3Oo3n64WuwV4Uo"
SHEET_NAME = "Participantes"

PARTICIPANTES = [
    "Pako", "Tanke", "Alice", "Pequeña Q", "Paco",
    "Silvia", "Mayte", "Q", "Yeyo", "Eliseo", "Oscar"
]


def _csv_url():
    return (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    )


def _leer_sheet() -> list[dict]:
    resp = requests.get(_csv_url(), timeout=15)
    resp.raise_for_status()
    reader = csv.DictReader(io.StringIO(resp.text))
    return list(reader)


def estado_wishlists() -> dict[str, bool]:
    try:
        filas = _leer_sheet()
        resultado = {}
        for fila in filas:
            nombre = fila.get("Nombre", "").strip()
            wishlist = fila.get("Wishlist", "").strip()
            if nombre in PARTICIPANTES:
                resultado[nombre] = bool(wishlist)
        for p in PARTICIPANTES:
            if p not in resultado:
                resultado[p] = False
        return resultado
    except Exception as e:
        print(f"[SHEETS ERROR] {e}")
        return {p: False for p in PARTICIPANTES}


def nombres_con_wishlist() -> list[str]:
    return [n for n, tiene in estado_wishlists().items() if tiene]


def nombres_sin_wishlist() -> list[str]:
    return [n for n, tiene in estado_wishlists().items() if not tiene]


def conteo() -> dict:
    estado = estado_wishlists()
    con = sum(1 for v in estado.values() if v)
    return {
        "total": len(PARTICIPANTES),
        "con_wishlist": con,
        "sin_wishlist": len(PARTICIPANTES) - con,
    }
