import re
import sensors

class DS18B20(sensors.Sensor):
    def __init__(self, id, position, device_id, correction_offset):
        super().__init__(id=id, type="DS18B20", position=position, accuracy=0.5, correction_offset=correction_offset) # is accuracy correct?
        self.file = open("/sys/bus/w1/devices/{}/w1_slave".format(device_id), "r")

    def __read__(self) -> float:
        raw_info = self.file.read()
        self.file.seek(0)

        search_results = re.findall(r"t=([0-9]+)", raw_info)

        if len(search_results) > 0:
            temp = int(search_results[0]) / 1000
            return temp
        else:
            return 0
