# EvilSanta-Bot 🎅🧝

Bot autónomo de WhatsApp para administrar el intercambio de regalos "La No Navidad".

## Qué hace

- Envía mensajes programados al grupo de WhatsApp entre Nov 26 y Dic 24
- Genera contenido dinámico (estado de wishlists, cuenta regresiva) consultando Google Sheets
- Notifica a Pako por DM con un preview antes de enviar al grupo
- Pako responde `SI` para aprobar — sin respuesta en 4h, se cancela

## Stack

- **Hosting**: Railway (cron job diario 9am CDMX = `0 15 * * *` UTC)
- **WhatsApp API**: [Whapi.cloud](https://whapi.cloud)
- **Datos**: Google Sheets (CSV export público, sin OAuth)
- **Lenguaje**: Python 3.11+

## Setup en Railway

1. New Project → Deploy from GitHub → `EvilSanta-Bot`
2. Variables de entorno:

| Variable | Valor |
|---|---|
| `WHAPI_TOKEN` | Token de Whapi.cloud |
| `WHAPI_GROUP_ID` | ID del grupo de WhatsApp |
| `PAKO_NUMERO` | `5215543391221` |

3. `railway.json` ya incluye el cron schedule `0 15 * * *` (9am CDMX).

## Flujo de aprobación

```
[Cron 9am] → main.py corre
    → ¿Hay mensaje pendiente de aprobación?
        → Revisa DMs de Pako
        → Si responde SI → envía al grupo ✅
        → Si timeout (4h) → cancela ❌
    → ¿Hay mensaje para hoy en el calendario?
        → Genera preview
        → Envía DM a Pako para aprobación
        → Guarda estado en state.json
```
