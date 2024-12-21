import asyncio
import websockets
from app.charge_point import ChargePoint
from config.settings import Config


async def start_websocket_client():
    """Start WebSocket connection for ChargePoint."""
    async with websockets.connect(
        f"ws://{Config.CENTRAL_SERVER_HOST}:{Config.CENTRAL_SERVER_PORT}/CP_1",
        subprotocols=["ocpp1.6"]
    ) as ws:
        cp = ChargePoint("CP_1", ws)
        await asyncio.gather(cp.start(), cp.send_boot_notification())
