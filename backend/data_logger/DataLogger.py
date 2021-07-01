import asyncio
from pathlib import Path
import io
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Union
from .CSVFileManager import CSVFileManager, Column as CSVColumn

class DataLogger(ABC):
  def __init__(self, sensor_manager, interval):
    self.sensor_manager = sensor_manager

    self.csv_file_manager = CSVFileManager(columns=[
      CSVColumn(data_key='timestamp_unix', title='timestamp(unix)', type=int),
      CSVColumn(data_key='timestamp_human', title='timestamp(human)', type=int)
    ] + [CSVColumn(data_key=sensor.id, title="{}:{}:{}:{}".format(sensor.id, sensor.type, sensor.position, sensor.accuracy), type=float) for sensor in self.sensor_manager.sensors])

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
  async def get_log_files_containing_interval(self, start: int, end: int) -> List[Union[Path, io.IOBase]]:
    """
    returns the paths to log files or the open log file objects that intersect with the given interval
    """

    pass

  @abstractmethod
  async def get_log_files(self) -> List[Union[Path, io.IOBase]]:
    """
    returns all the paths to log files or the open log file objects stored by this data logger
    """

    pass

  async def make_sensor_values_csv_line(self, timestamp, values):
    csv = ""
    csv += str(timestamp)
    csv += ","
    csv += str(datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S %d.%m.%Y'))
    csv += ","

    for sensor in self.sensor_manager.sensors:
      sensor_value = values[sensor.id]
      csv += str(sensor_value)
      csv += ","
    csv += "\n"

    return csv