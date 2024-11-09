from ManagerPeriferic import ManagerPeriferic

if __name__ == "__main__":
    tester = ManagerPeriferic()

    tester.add_periferic("00001", 9.5, 8.5, True, 0, "rtsp://192.168.18.68:8080/h264_ulaw.sdp")
    tester.add_periferic("00002", 9.5, 8.5, True, 0, "rtsp://192.168.18.68:8080/h264_ulaw.sdp")
