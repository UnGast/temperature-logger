import asyncio
from pathlib import Path
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
  async def get_past_data(self, start: int, end: int):
    """
    get historical data between two unix timestamps
    """

    pass

  @abstractmethod
  async def get_log_files_containing_interval(self, start: int, end: int) -> [Path]:
    """
    returns the file paths that intersect with the given interval
    """

    pass

  @abstractmethod
  async def get_log_files(self) -> [Path]:
    """
    returns all the files stored by this data logger
    """

    pass