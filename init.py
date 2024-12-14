import time
from RtspStream import RtspStream
from Sensor import Sensor
from ManagerPeriferic import ManagerPeriferic
from multiprocessing import Manager
from config import *
import asyncio
import yaml

def load_data():
    # Crear el diccionario compartido
    shared_map = Manager().dict()
    tester = ManagerPeriferic()
    
    # Leer el archivo YAML
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)

    # Crear listas de objetos Camara y Sensor
    periferics = data.get("periferics", {})

    cam_map = {item["id"]: RtspStream(item["id"], item["latitud"], item["longitud"], item["power_on"], 
                            item["state"], item["url"], shared_map) for item in periferics.get("Camara", [])}

    for camera in cam_map.values():
        camera.start_conection()
        tester.add_periferic(camera)

    arr = []

    for item in periferics.get("Sensor", []):
        sensor = Sensor(item["id"], item["latitud"], item["longitud"], item["power_on"], item["state"], 
                        item["url"])

        sensor.set_controler(shared_map)

        for camera_id in item.get("subscribe_to_cameras", []):
            sensor.attach(cam_map[camera_id])

        tester.add_periferic(sensor)
        arr.append(sensor)

    [s.start_capture() for s in arr]

    return shared_map, tester


