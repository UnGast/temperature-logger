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

      data_entry = { 'timestamp': i }

      for sensor in self.sensor_manager.sensors:
        
        data_entry[sensor.id] = math.sin(i)

      data.append(data_entry)

    return data