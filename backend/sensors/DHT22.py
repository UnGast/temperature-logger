import adafruit_dht
import board
import sensors

class DHT22(sensors.Sensor):

    def __init__(self, id, position, pin):
        
        super().__init__(id=id, type="DHT22", position=position, accuracy=0.5) # is accuracy correct?

        prepared_pin = pin
        
        if isinstance(pin, str):
            
            prepared_pin = getattr(board, pin)
                        
        self.backend = adafruit_dht.DHT22(prepared_pin)

    def read(self):
        
        return self.backend.temperature