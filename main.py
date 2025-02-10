import asyncio
from threading import Thread
from app.websocket_client import start_websocket_client
from app.http_server import create_http_server
from config.settings import Config
from app.charge_point import ChargePoint

from flask import Flask

def run_http_server(cp_instance):
    """Run the HTTP server in a separate thread."""
    app = create_http_server(cp_instance)
    app.run(host=Config.HTTP_SERVER_HOST, port=Config.HTTP_SERVER_PORT)

async def main():
    """Start the WebSocket client and HTTP server."""
    # Create a ChargePoint instance
    cp_instance = ChargePoint("CP_1", None)  # Pass None initially for the WebSocket

    # Start the HTTP server in a separate thread
    http_thread = Thread(target=run_http_server, args=(cp_instance,))
    http_thread.start()

    # Start the WebSocket client
    await start_websocket_client()

    # await asyncio.wait([asyncio.create_task(run_http_server(cp_instance)), asyncio.create_task(await start_websocket_client())])

if __name__ == "__main__":
    asyncio.run(main())
