import random
from datetime import datetime
from zoneinfo import ZoneInfo

CDMX = ZoneInfo("America/Mexico_City")

VENTANA_NORMAL   = (9, 14)
VENTANA_ACERTIJO = (12, 18)
VENTANA_BROMA    = (21, 23)

ELFSTER_URL = "https://www.elfster.com/gift-exchange-generator/5469eeb1-7bb6-44e1-a09c-f661ca81d3f0/participants?fsimple=true&draw=true"


def generar_reconocimiento(nombres: list[str]) -> str:
    if not nombres:
        return (
            "📋 *Estado de wishlists*\n\n"
            "Nadie ha subido su wishlist todavía... 👀\n"
            "¡Sean los primeros! El tiempo corre 🎄"
        )
    lista = "\n".join(f"  ✅ {n}" for n in nombres)
    return (
        f"🌟 *Shoutout navideño* 🌟\n\n"
        f"Estos elfos ya tienen su wishlist lista:\n{lista}\n\n"
        f"El resto... el Elf on the Shelf los está viendo 👀🧝"
    )


def generar_estado_sistema(total: int, con_wishlist: int, dias_restantes: int) -> str:
    sin = total - con_wishlist
    barra = "🟢" * con_wishlist + "🔴" * sin
    return (
        f"🎄 *Sistema EvilSanta — Reporte de Status* 🎄\n\n"
        f"Elfos registrados: {total}\n"
        f"Wishlists completas: {con_wishlist}/{total}\n"
        f"{barra}\n\n"
        f"⏳ Días para el intercambio: *{dias_restantes}*\n"
        f"No dejen para mañana lo que el Elf on the Shelf puede reportar hoy 🧝"
    )


def generar_cuenta_regresiva(dias: int) -> str:
    frases = [
        f"⏰ Faltan solo *{dias} días* para el intercambio. ¿Ya compraron?",
        f"🎁 *{dias} días* y contando... el tiempo vuela más rápido que Santa 🦌",
        f"🚨 Alerta EvilSanta: *{dias} días* restantes. No hay excusas 🎅",
    ]
    return random.choice(frases)


CALENDARIO = [
    (
        "elf_wanted_1",
        (11, 26),
        VENTANA_NORMAL,
        "🧝 *WANTED: Elf on the Shelf*\n\nSe busca elfo perdido en esta familia. Última vez visto: revisando wishlists.\n\nSi aún no has subido la tuya al sheet, el elfo YA sabe quién eres.\n\nEnlace Elfster 👇\n" + ELFSTER_URL,
    ),
    ("reconocimiento_1", (11, 28), VENTANA_NORMAL, None),
    (
        "deadline_cierre",
        (11, 28),
        VENTANA_ACERTIJO,
        "⏰ *Recordatorio: cierre de wishlists HOY*\n\nEl sistema EvilSanta cierra registro de wishlists esta noche.\nDespués de las 11pm, el elfo toma nota de los ausentes.\n\nÚltima oportunidad 👇\n" + ELFSTER_URL,
    ),
    ("estado_sistema_1", (11, 30), VENTANA_NORMAL, None),
    (
        "elf_shell_1",
        (12, 2),
        VENTANA_BROMA,
        "🧝💻 *Elf on a Shell #1*\n\n```\n$ elf --check-wishlist --all\nScanning participants...\n✅ Pako        [wishlist: found]\n❓ ???         [wishlist: missing]\n❓ ???         [wishlist: missing]\n\nWARNING: 2 naughty nodes detected\nRunning: notify-santa --priority=HIGH\n```\n\nEl elfo ya ejecutó el script. Santa tiene el log 🎅",
    ),
    ("estado_sistema_2", (12, 7), VENTANA_NORMAL, None),
    (
        "rickroll_navidad",
        (12, 9),
        VENTANA_BROMA,
        "🎵 *Pista musical del intercambio*\n\nLes comparto la canción oficial de esta temporada...\n\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ\n\n(El elfo no se disculpa 🧝🎄)",
    ),
    (
        "elf_shell_2",
        (12, 11),
        VENTANA_BROMA,
        "🧝💻 *Elf on a Shell #2*\n\n```\n$ santa-audit --naughty-list --verbose\nConnecting to North Pole API...\nAuthentication: OK\nQuerying gift database...\n\n[ALERT] Gift budget anomaly detected\n[ALERT] Regift probability: 34%\n[ALERT] Running: shame --public --group-chat\n\nNotification sent. Ho ho ho.\n```\n\n¿Quién tiene 34% de regifting? El elfo lo sabe 👀",
    ),
    ("estado_sistema_3", (12, 14), VENTANA_NORMAL, None),
    (
        "reto_envoltura",
        (12, 16),
        VENTANA_NORMAL,
        "🎁 *Reto de envoltura navideña*\n\nEl Elf on the Shelf lanza el reto oficial:\n\nEnvía foto de tu regalo envuelto antes del 23 de diciembre.\nEl mejor envuelto gana... el respeto eterno del grupo 🏆\n\n(Y probablemente un meme de premio del elfo 🧝)",
    ),
    ("cuenta_regresiva_3", (12, 21), VENTANA_NORMAL, None),
    (
        "instrucciones_dia",
        (12, 23),
        VENTANA_NORMAL,
        "📋 *Instrucciones para mañana — Día del Intercambio*\n\n🕐 Hora: la que acordamos\n📍 Lugar: el que acordamos\n🎁 Lleva: tu regalo envuelto con el nombre del destinatario\n\nEl Elf on the Shelf estará presente (y tomando fotos comprometedoras).\n\n¡Nos vemos mañana familia! 🎄🎅",
    ),
    (
        "activacion_final",
        (12, 24),
        VENTANA_NORMAL,
        "🎄🎅 *¡Feliz Navidad, familia EvilSanta!* 🎅🎄\n\nHoy es el día. El Elf on the Shelf cumplió su misión.\nEspero que sus regalos sean tan buenos como sus excusas para no subir la wishlist.\n\nQue la magia de la Navidad (y el regalo correcto) estén con ustedes.\n\n*EvilSanta-Bot, cerrando operaciones hasta el próximo año* 🧝✌️",
    ),
]


def get_mensaje_hoy(ahora: datetime = None) -> tuple[str, str] | None:
    if ahora is None:
        ahora = datetime.now(CDMX)

    hoy = (ahora.month, ahora.day)
    hora = ahora.hour

    for clave, fecha, (h_ini, h_fin), contenido in CALENDARIO:
        if fecha != hoy:
            continue
        if not (h_ini <= hora < h_fin):
            continue

        if contenido is None:
            if clave.startswith("reconocimiento"):
                from sheets import nombres_con_wishlist
                contenido = generar_reconocimiento(nombres_con_wishlist())
            elif clave.startswith("estado_sistema"):
                from sheets import conteo
                c = conteo()
                dia_intercambio = datetime(ahora.year, 12, 24, tzinfo=CDMX)
                dias = (dia_intercambio - ahora).days
                contenido = generar_estado_sistema(
                    c["total"], c["con_wishlist"], max(dias, 0)
                )
            elif clave.startswith("cuenta_regresiva"):
                dia_intercambio = datetime(ahora.year, 12, 24, tzinfo=CDMX)
                dias = (dia_intercambio - ahora).days
                contenido = generar_cuenta_regresiva(max(dias, 0))

        if contenido:
            return clave, contenido

    return None
