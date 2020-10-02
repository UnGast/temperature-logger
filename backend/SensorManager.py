from abc import ABC, abstractmethod

class SensorManager(ABC):

    def __init__(self, sensors):

        self.sensors = sensors

    async def get_latest_values(self):

        return dict([(s.id, s.last_value()) for s in self.sensors])