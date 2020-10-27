import asyncio
import time
import os
import math
from pathlib import Path
from .DataLogger import DataLogger
from .CSVFileManager import CSVFileManager, Column as CSVColumn
from SensorManager import SensorManager

class DefaultDataLogger(DataLogger):
  def __init__(self, sensor_manager: SensorManager, interval: int, file_interval: int, directory: str):
    super().__init__(sensor_manager=sensor_manager, interval=interval)

    self.directory = Path(directory)
    self.csv_file_manager = CSVFileManager(columns=[
      CSVColumn(data_key='timestamp', title='timestamp(unix)', type=int)
    ] + [CSVColumn(data_key=sensor.id, title="{}:{}:{}:{}".format(sensor.id, sensor.type, sensor.position, sensor.accuracy), type=float) for sensor in self.sensor_manager.sensors])

    self.log_start_timestamp = None
    self.current_file_timestamp = None

    if file_interval < 1:
       raise Exception("file interval cannot be smaller than 1")

    self.file_interval = file_interval # after how many seconds start a new file
    self.opened_file = None
    self.opened_file_timestamp = None
    self.previous_stored_sensor_values = None

  def __del__(self):
    print("Destruct DefaultDataLogger")
    if self.opened_file is not None:
      self.opened_file.close()

  async def log_loop(self):
    if self.log_start_timestamp is None:
      self.log_start_timestamp = await self.get_log_start_timestamp()

    while True:
      current_timestamp = int(time.time())
      current_sensor_values = await self.get_current_sensor_data()
      sensor_values_changed = current_sensor_values != self.previous_stored_sensor_values
      new_file_created = False

      # returned true means a new file was created
      if await self.ensure_timestamp_containing_file_opened(current_timestamp):
        self.opened_file.write(self.get_log_file_csv_header())
        new_file_created = True

      if new_file_created or sensor_values_changed:
        new_csv_line = await self.make_sensor_values_csv_line(current_timestamp, current_sensor_values)
        self.opened_file.write(new_csv_line)
        self.previous_stored_sensor_values = current_sensor_values

      await asyncio.sleep(self.interval)

  async def get_past_data(self, start, end):
    log_files = await self.get_log_files_containing_interval(start, end)
    past_data = []

    for file in log_files:
      file_data = self.csv_file_manager.read_file(file)

      for line_data in file_data:
        timestamp = int(line_data['timestamp'])

        if timestamp >= start and timestamp <= end:
          past_data.append(line_data)

    return past_data

  async def get_log_files_containing_interval(self, start: int, end: int):
    log_files = await self.get_log_files()
    filtered_files = []
    
    for file in log_files:
      timestamps = self.get_log_file_timestamps(file)

      if (timestamps['start'] >= start and timestamps['start'] <= end) \
        or (timestamps['end'] >= start and timestamps['end'] <= end) \
          or (timestamps['start'] <= start and timestamps['end'] >= end):

            filtered_files.append(file)

    return filtered_files

  async def get_log_files(self):
    return list(self.directory.glob('*.csv'))

  def get_log_file_timestamps(self, file_path) -> { 'start', 'end' }:
    parts = file_path.stem.split('-')
    return { 'start': int(parts[0]), 'end': int(parts[1]) }

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
      interval_start = self.get_log_file_timestamps(file)['start'] #int(interval_string.split('-')[0])
      if min_interval_start is None or interval_start < min_interval_start:
        min_interval_start = interval_start

    return min_interval_start

  async def get_containing_file_timestamp(self, contained_timestamp):
    contained_timestamp = int(time.time())
    time_since_log_start = contained_timestamp - self.log_start_timestamp
    interval_index = math.floor(time_since_log_start / self.file_interval)
    file_timestamp = self.log_start_timestamp + self.file_interval * interval_index
    return file_timestamp

  async def ensure_timestamp_containing_file_opened(self, contained_timestamp) -> bool:
    containing_file_timestamp = await self.get_containing_file_timestamp(contained_timestamp)

    if self.opened_file_timestamp != containing_file_timestamp:
      if self.opened_file is not None:
        self.opened_file.close()

      filepath = self.get_filepath_for_timestamp(containing_file_timestamp)
      if not filepath.parent.exists():
        os.makedirs(filepath.parent)

      file_existed = filepath.exists()
      self.opened_file = open(filepath, 'a')
      self.opened_file_timestamp = containing_file_timestamp

      return not file_existed

  def get_filepath_for_timestamp(self, timestamp):
    end_timestamp = timestamp + self.file_interval
    return self.directory/"{}-{}.csv".format(timestamp, end_timestamp)

  async def get_current_sensor_data(self):
    return await self.sensor_manager.get_latest_values()

  async def make_sensor_values_csv_line(self, timestamp, values):
    csv = ""
    csv += str(timestamp)
    csv += ","

    for sensor in self.sensor_manager.sensors:
      sensor_value = values[sensor.id]
      csv += str(sensor_value)
      csv += ","
    csv += "\n"

    return csv

  def get_log_file_csv_header(self) -> str:
    csv = "timestamp(unix)"
    csv += ","

    for sensor in self.sensor_manager.sensors:
      csv += "{}:{}:{}:{}".format(sensor.id, sensor.type, sensor.position, sensor.accuracy)
      csv += ","
    csv += "\n"

    return csv