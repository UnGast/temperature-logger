import math
import asyncio
from .DataLogger import DataLogger

class MockDataLogger(DataLogger):

  async def log_loop(self):

    while True:

      print("would log data if it wasn't a mock")

      await asyncio.sleep(self.interval)

  async def get_past_data(self, start: int, end: int):

    data = []

    for i in range(start, end, 10):

      for sensor in self.sensor_manager.sensors:

        data.append({ "sensorId": sensor.id, "timestamp": i, "value": math.sin(i) })

    return data