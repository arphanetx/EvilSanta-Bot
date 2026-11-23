import os
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from whapi import enviar_dm, enviar_al_grupo, leer_mensajes_dm
from sheets import nombres_con_wishlist, nombres_sin_wishlist, conteo
from messages import get_mensaje_hoy

CDMX = ZoneInfo("America/Mexico_City")
PAKO_NUMERO = os.environ.get("PAKO_NUMERO", "5215543391221")
PAKO_DM = f"{PAKO_NUMERO}@s.whatsapp.net"
TIMEOUT_APROBACION_HORAS = 4
STATE_FILE = Path(__file__).parent / "state.json"


def cargar_estado():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def guardar_estado(estado):
    with open(STATE_FILE, "w") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)


def revisar_aprobacion_pendiente(estado):
    if "pendiente" not in estado:
        return False

    pendiente = estado["pendiente"]
    ahora = datetime.now(CDMX)
    creado = datetime.fromisoformat(pendiente["creado_en"])
    horas_transcurridas = (ahora - creado).total_seconds() / 3600

    mensajes = leer_mensajes_dm(PAKO_DM, limit=10)
    for msg in mensajes:
        texto = msg.get("text", {}).get("body", "").strip().upper()
        timestamp = msg.get("timestamp", 0)
        if timestamp > creado.timestamp():
            if texto in ["SI", "SÍ", "YES", "OK", "S"]:
                enviar_al_grupo(pendiente["mensaje"])
                print(f"[OK] Mensaje enviado al grupo tras aprobacion de Pako")
                del estado["pendiente"]
                estado.setdefault("enviados", []).append(pendiente["clave"])
                guardar_estado(estado)
                return True

    if horas_transcurridas > TIMEOUT_APROBACION_HORAS:
        print(f"[TIMEOUT] Aprobacion expirada para clave {pendiente['clave']}")
        del estado["pendiente"]
        guardar_estado(estado)
        return False

    print(f"[ESPERA] Pendiente de aprobacion ({horas_transcurridas:.1f}h transcurridas)")
    return False


def main():
    ahora = datetime.now(CDMX)
    print(f"[EvilSanta] Corriendo: {ahora.strftime('%Y-%m-%d %H:%M')} CDMX")

    estado = cargar_estado()

    if "pendiente" in estado:
        revisar_aprobacion_pendiente(estado)
        return

    resultado = get_mensaje_hoy(ahora)
    if resultado is None:
        print("[INFO] No hay mensaje programado para hoy en esta hora.")
        return

    clave, mensaje = resultado

    enviados = estado.get("enviados", [])
    if clave in enviados:
        print(f"[SKIP] '{clave}' ya fue enviado.")
        return

    preview = (
        f"🎅 *EvilSanta-Bot | Preview*\n"
        f"Clave: `{clave}`\n"
        f"Fecha: {ahora.strftime('%d/%m/%Y %H:%M')}\n\n"
        f"---\n{mensaje}\n---\n\n"
        f"Responde *SI* para enviar al grupo."
    )
    enviar_dm(PAKO_DM, preview)
    print(f"[DM] Preview enviado a Pako para aprobacion: {clave}")

    estado["pendiente"] = {
        "clave": clave,
        "mensaje": mensaje,
        "creado_en": ahora.isoformat(),
    }
    guardar_estado(estado)


if __name__ == "__main__":
    main()
