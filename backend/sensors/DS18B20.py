import re
import sensors

class DS18B20(sensors.Sensor):
    
    def __init__(self, id, position):

        super().__init__(id=id, name="DS18B20", position=position, accuracy=0.5) # is accuracy correct?

        self.file = open("/sys/bus/w1/devices/{}/w1_slave".format(id), "r")

    def read(self):

        raw_info = self.file.read()
        
        self.file.seek(0)

        temp = int(re.findall(r"t=([0-9]+)", raw_info)[0]) / 1000

        return temp