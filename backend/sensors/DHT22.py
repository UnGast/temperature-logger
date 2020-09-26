import adafruit_dht
import sensors

class DHT22(sensors.Sensor):

    def __init__(self, id, position, pin):

        super().__init__(id=id, type="DHT22", position=position, accuracy=0.5) # is accuracy correct?

        self.backend = adafruit_dht.DHT22(pin)

    def read(self):

        return self.backend.temperature