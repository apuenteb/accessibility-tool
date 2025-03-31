"""
REQUIREMENTS:
    fastapi uvicorn websockets requests websocket_client
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
import uvicorn
import os
import json
import multiprocessing
import requests
import threading

import websocket

from typing import Optional

STARTUP_MESSAGE = """{"type":"TABLE_SNAPSHOT","content":{"GEOGRID":{"features":[],"type":"FeatureCollection","properties":{"header":{"tableName":"_","latitude":43.317645,"longitude":-2.005646,"tz":"1","nrows":1,"ncols":1,"rotation":0,"cellSize":1,"projection":"+proj=lcc +lat_1=42.68333333333333 +lat_2=41.71666666666667 +lat_0=41 +lon_0=-71.5 +x_0=200000 +y_0=750000 +ellps=GRS80 +datum=NAD83 +units=m +no_def"},"types":{}}},"GEOGRIDDATA":[]}}"""
def setup_server() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Serve projection mapping
    app.mount("/CS_cityscopeJS_projection_mapping/static", StaticFiles(directory="./projection_mapping/static"), name="static")
    @app.get("/")
    async def serve_react_root():
        return FileResponse(os.path.join("./projection_mapping", "index.html"))

    # Store active WebSocket connections
    connections = set()

    # Ws endpoint
    @app.websocket("/map_ws")
    async def websocket_endpoint(websocket: WebSocket):
        """Handle WebSocket connections"""
        await websocket.accept()
        connections.add(websocket)
        try:
            await websocket.send_text(STARTUP_MESSAGE)
            while True:
                data = await websocket.receive_text()
                print(f"Message received: {data}", flush=True)
        except WebSocketDisconnect:
            print("Connection Removed", flush=True)
            connections.remove(websocket)

    async def send_geojson(geojson: dict):
        """Send geojson data to all active WebSocket connections."""
        if not connections:
            print("No active WebSocket connections")
            return

        mapped_geojson = {
            "content": {
                "gridId": "nombre_de_la_mesa",
                "save": False,
                "moduleData": {
                    "layers": [{
                        "type": "geojson",
                        "data": geojson,
                        "properties": {},
                    }],
                    "numeric": [],
                },
            },
            "type": "MODULE"
        }

        for connection in connections:
            await connection.send_text(json.dumps(mapped_geojson))

    @app.post("/send_geojson")
    async def send_geojson_api(geojson: dict):
        """Expose an API to send GeoJSON data externally."""

        await send_geojson(geojson)
        return {"message": "GeoJSON sent to all clients"}

    return app

def start_local():
    app = setup_server()
    uvicorn.run(app, host="127.0.0.1", port=9999)

def send_geojson_sync(geojson: dict):
    requests.post("http://127.0.0.1:9999/send_geojson", json=geojson)

class CityIo:

    server_url: str = "wss://cityio.media.mit.edu/cityio/module"

    def __init__(self, table_name: Optional[str] = None, is_local: bool = False):
        self.is_local: bool = is_local
        if not self.is_local:
            self.ws = None
            self.table_name = table_name
            self.connected_event = threading.Event()

    def _send(self, message: dict):
        thread = threading.Thread(target=lambda: self.ws.send(json.dumps(message)))
        thread.start()

    def _on_open(self, _ws):
        self.connected_event.set()

    def _send_layers(self, layers: list[dict]):
        layers_message = {
            "type": "MODULE",
            "content": {
                "gridId": self.table_name,
                "save": False,
                "moduleData": {
                    "layers": layers
                }
            }
        }
        self._send(layers_message)

    def _start_websocket(self):
        self.ws = websocket.WebSocketApp(self.server_url, on_open=self._on_open)
        self.ws.run_forever()

    def start(self):
        if self.is_local:
            server_process = multiprocessing.Process(target=start_local, daemon=True)
            server_process.start()
        else:
            ws_thread = threading.Thread(target=self._start_websocket)
            ws_thread.daemon = True
            ws_thread.start()

            self.connected_event.wait()

    def send_geojson(self, geojson: dict):
        if self.is_local:
            thread = threading.Thread(target=lambda: send_geojson_sync(geojson))
            thread.start()
        else:
            geojson_message = [{
                "type": "geojson",
                "data": geojson,
                "properties": {}
            }]
            self._send_layers(geojson_message)
