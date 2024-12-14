# WatchCodes

## Installation
Install the dependencies with pip(Python).

```sh
pip install -r requirements.txt
```

Open file config.yaml

Here, you can personalize the parameters as needed. It is very important to change the **camera URL**, as well as the transmission IP address for the camera.


```yaml
periferics:
  Camara:
    - id: "0001"
      latitud: 9.5
      longitud: 8.5
      power_on: true
      state: 0
      url: "rtsp://192.168.18.93:8080/h264_ulaw.sdp"

    - id: "0002"
      latitud: 10.5
      longitud: 7.5
      power_on: false
      state: 1
      url: "rtsp://192.168.18.93:8080/h264_ulaw.sdp"

  Sensor:
    - id: "0003"
      latitud: 9.5
      longitud: 8.5
      power_on: true
      state: 0
      url: "http://192.168.18.93/sensor1"
      subscribe_to_cameras:
        - "0001"
        - "0002"

```

Open your favorite Terminal and run these commands.


```sh
python3 Game.py
```

## Docker

```sh
pendiente
```

## License

UNI
**Free Software, Hell Yeah!**
