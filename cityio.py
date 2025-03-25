import websocket
import json
import threading

class CityIo:
    
    server_url: str = "wss://cityio.media.mit.edu/cityio/module"
    
    def __init__(self, table_name: str):
        self.ws = None
        self.table_name = table_name
        self.connected_event = threading.Event()
        
    def _send(self, message: dict):
        self.ws.send(json.dumps(message))
        
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
    
    def send_geojson(self, geojson: dict):
        """Utility function to send a single geojson,
        this function does not batch and should only be used if only sending a single geojson layer"""
        
        geojson_message = [{
            "type": "geojson",
            "data": geojson,
            "properties": {}
        }]
        self._send_layers(geojson_message)
        
    def _start_websocket(self):
        self.ws = websocket.WebSocketApp(self.server_url, on_open=self._on_open)
        self.ws.run_forever()
    
    def start(self):
        ws_thread = threading.Thread(target=self._start_websocket)
        ws_thread.daemon = True
        ws_thread.start()
        
        self.connected_event.wait()
