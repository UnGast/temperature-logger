import asyncio

class DataLogger():

  def __init__(self, sensor_manager, interval):

    self.sensor_manager = sensor_manager

    self.interval = interval

  async def log_loop(self):

    while True:

      print("LOG DATA")

      await asyncio.sleep(self.interval)