from fastapi import FastAPI, BackgroundTasks
from ManagerRtspStream import ManagerRtspStream
from pydantic import BaseModel
import time
from concurrent.futures import ThreadPoolExecutor
import sys
app = FastAPI()
manager = ManagerRtspStream()
executor = ThreadPoolExecutor()

class URLRequest(BaseModel):
    url: str

def capture_task(url: str):
    camera = manager.add_prueba(url)
    if camera.start_conection():
        print("Se conecto :) ")
        camera.start_capture()
        print("Inicio captura")

        start_time = time.time()
        while (time.time() - start_time) < 20:  # Capture for 20 seconds
            for url in manager.shared_map.keys():
                frame = manager.shared_map[url]
                print(frame)

            time.sleep(0.03)
        camera.stop_capture()
        print(f"Capture completed for {url}")

@app.post("/start_stream/")
def start_stream(request: URLRequest, background_tasks: BackgroundTasks):
    try:
        url = request.url
        background_tasks.add_task(executor.submit, capture_task, url)
        return {"status": "success", "message": f"Stream started for {url}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}