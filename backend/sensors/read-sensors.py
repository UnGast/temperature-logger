import time
import board
import adafruit_dht
import re

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
