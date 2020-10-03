from abc import ABC, abstractmethod

class SensorManager(ABC):

    def __init__(self, sensors):

        self.sensors = sensors

    async def get_latest_values(self):
        
        values = {}
        
        for sensor in self.sensors:
            
            try:
                
                values[sensor.id] = sensor.read()
            
            except Exception as e:

                print("could not read value for sensor", sensor, e)
                
                values[sensor.id] = 0
                
        return values
