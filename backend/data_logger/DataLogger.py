import asyncio
from abc import ABC, abstractmethod

class DataLogger(ABC):

  def __init__(self, sensor_manager, interval):

    self.sensor_manager = sensor_manager

    if interval < 1:

      raise Exception("DataLogger interval cannot be smaller than 1")

    self.interval = interval

  @abstractmethod
  async def log_loop(self):

    pass

  @abstractmethod
  async def get_past_data(self, start: int, end: int) -> [{'sensor_id': int, 'timestamp': int, 'value': float}]:
    """
    get historical data between two unix timestamps
    """

    pass