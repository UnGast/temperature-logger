import asyncio
from .DataLogger import DataLogger
from SensorManager import SensorManager

class DefaultDataLogger(DataLogger):

  def __init__(self, sensor_manager: SensorManager, interval: int, file_path: str):

    super().__init__(sensor_manager=sensor_manager, interval=interval)

    self.file_path = file_path

  async def log_loop(self):

    while True:

      print("LOG DATA")

      await asyncio.sleep(self.interval)