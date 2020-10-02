import asyncio
import time
import os
import math
from pathlib import Path
from .DataLogger import DataLogger
from SensorManager import SensorManager

class DefaultDataLogger(DataLogger):

  def __init__(self, sensor_manager: SensorManager, interval: int, directory: str):

    super().__init__(sensor_manager=sensor_manager, interval=interval)

    self.directory = Path(directory)

    self.log_start_timestamp = None

    self.current_file_timestamp = None

    self.file_interval = 2 # after how many seconds start a new file

    self.opened_file = None

    self.opened_file_timestamp = None

  def __del__(self):

    print("Destruct DefaultDataLogger")

    if self.opened_file is not None:

      self.opened_file.close()

  async def log_loop(self):

    if self.log_start_timestamp is None:

      self.log_start_timestamp = await self.get_log_start_timestamp()

    while True:

      current_timestamp = int(time.time())

      new_data_line = await self.get_current_sensor_data_csv_line()

      await self.ensure_timestamp_containing_file_opened(current_timestamp)
      
      self.opened_file.write(new_data_line)

      await asyncio.sleep(self.interval)

  async def get_past_data(self, start, end):

    return []

  async def get_log_files(self):

    return list(self.directory.glob('*.csv'))

  """
  Returns the timestamp of the first log file.
  """
  async def get_log_start_timestamp(self) -> int:
    
    files = await self.get_log_files()

    if len(files) == 0:

      return int(time.time())

    min_interval_start = None

    for file in files:

      interval_string = file.stem

      interval_start = int(interval_string.split('-')[0])

      if min_interval_start is None or interval_start < min_interval_start:

        min_interval_start = interval_start

    return min_interval_start

  async def get_containing_file_timestamp(self, contained_timestamp):

    contained_timestamp = int(time.time())

    time_since_log_start = contained_timestamp - self.log_start_timestamp

    interval_index = math.floor(time_since_log_start / self.file_interval)

    file_timestamp = self.log_start_timestamp + self.file_interval * interval_index

    return file_timestamp

  async def ensure_timestamp_containing_file_opened(self, contained_timestamp):

    containing_file_timestamp = await self.get_containing_file_timestamp(contained_timestamp)

    if self.opened_file_timestamp != containing_file_timestamp:

      if self.opened_file is not None:

        self.opened_file.close()

      filepath = self.get_filepath_for_timestamp(containing_file_timestamp)

      if not filepath.parent.exists():

        os.makedirs(filepath.parent)

      self.opened_file = open(filepath, 'a')

      self.opened_file_timestamp = containing_file_timestamp

      self.opened_file.write(self.get_log_file_csv_header())

  def get_filepath_for_timestamp(self, timestamp):

    end_timestamp = timestamp + self.file_interval

    return self.directory/"{}-{}.csv".format(timestamp, end_timestamp)

  async def get_current_sensor_data(self):

    return await self.sensor_manager.get_latest_values()

  async def get_current_sensor_data_csv_line(self):

    data = await self.get_current_sensor_data()

    csv = ""

    for sensor in self.sensor_manager.sensors:

      sensor_data = data[sensor.id]
        
      csv += str(sensor_data['value']) + ","

    csv += "\n"

    return csv

  def get_log_file_csv_header(self) -> str:

    csv = ""

    for sensor in self.sensor_manager.sensors:

      csv += "{}:{}:{}:{}".format(sensor.id, sensor.type, sensor.position, sensor.accuracy)

      csv += ","

    csv += "\n"

    return csv