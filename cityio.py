# fastapi uvicorn websockets requests

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

STARTUP_MESSAGE = """{"type":"TABLE_SNAPSHOT","content":{"GEOGRID":{"features":[],"type":"FeatureCollection","properties":{"header":{"tableName":"_","latitude":43.317645,"longitude":-2.005646,"tz":"1","nrows":1,"ncols":1,"rotation":0,"cellSize":1,"projection":"+proj=lcc +lat_1=42.68333333333333 +lat_2=41.71666666666667 +lat_0=41 +lon_0=-71.5 +x_0=200000 +y_0=750000 +ellps=GRS80 +datum=NAD83 +units=m +no_def"},"types":{}}},"GEOGRIDDATA":[]}}"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/CS_cityscopeJS_projection_mapping/static", StaticFiles(directory="./projection_mapping/static"), name="static")

@app.get("/")
async def serve_react_root():
    return FileResponse(os.path.join("./projection_mapping", "index.html"))

# Store active WebSocket connections
connections = set()

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

def start():
    uvicorn.run(app, host="127.0.0.1", port=9999)

def send_geojson_sync(geojson: dict):
    """Blocking function to send GeoJSON from external scripts"""
    requests.post("http://127.0.0.1:9999/send_geojson", json=geojson)

server_process = multiprocessing.Process(target=start, daemon=True)
server_process.start()

class CityIo:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        pass

    def send_geojson(self, geojson: dict):
        thread = threading.Thread(target=lambda: send_geojson_sync(geojson))
        thread.start()
