import json
import asyncio
from websockets.sync.client import connect

jsonric = {"type": "setData", "param1": 0, "param2": 2.3}

def hello():
    with connect("ws://192.168.0.8:8765") as websocket:
        websocket.send("Hello world!")
        websocket.send(json.dumps(jsonric))

hello()