import time
import board
import adafruit_dht
import re

class Sensor:
    
    def __init__(self, name, position, accuracy):
        
        self.name = name

        self.position = position

        self.accuracy = accuracy

    def read():

        print("READ NOT IMPLEMENTED FOR SENSOR: {}".format(name))

class DHT22(Sensor):

    def __init__(self, position, pin):

        super().__init__(name="DHT22", position=position, accuracy=0.5) # is accuracy correct?

        self.backend = adafruit_dht.DHT22(pin)

    def read(self):

        return self.backend.temperature

class DS18B20(Sensor):
    
    def __init__(self, position, id):

        super().__init__(name="DS18B20", position=position, accuracy=0.5) # is accuracy correct?

        self.file = open("/sys/bus/w1/devices/{}/w1_slave".format(id), "r")

    def read(self):

        raw_info = self.file.read()
        
        self.file.seek(0)

        temp = int(re.findall(r"t=([0-9]+)", raw_info)[0]) / 1000

        return temp

sensors = [

   DHT22(position="Behind the oven", pin=board.D4),

   DS18B20(position="Somewhere else", id="28-0300a279abec"),
 
   DS18B20(position="Somewhere else", id="28-0300a279234e")
]

while True:

    for sensor in sensors:

        try:

            temperature = sensor.read()

            print("Sensor {} at {} reports temperature of {}°C".format(sensor.name, sensor.position, temperature))

        except Exception as e:

            print("While trying to measure sensor {} at {} an error occured".format(sensor.name, sensor.position), e)

    time.sleep(2.0)
