import asyncio
import time
import datetime
import os
import math
from pathlib import Path
from typing import Dict
from .DataLogger import DataLogger
from .CSVFileManager import CSVFileManager, Column as CSVColumn
from sensor_manager import SensorManager

class DefaultDataLogger(DataLogger):
  def __init__(self, sensor_manager: SensorManager, interval: int, file_interval: int, directory: str):
    super().__init__(sensor_manager=sensor_manager, interval=interval)

    self.directory = Path(directory)

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
        self.opened_file.write(self.csv_file_manager.get_csv_header() + '\n')
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
        try:
            timestamp = int(line_data['timestamp_unix'])

            if timestamp >= start and timestamp <= end:
              past_data.append(line_data)
        except Exception as e:
            print('warning could not read line in file data', line_data, 'because:', e)

    return past_data

  async def get_log_files_containing_interval(self, start: int, end: int):
    """
    Return all log files of which the data record time interval overlaps with the given time interval.
    """
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

  def get_log_file_timestamps(self, file_path) -> Dict[str, int]:
    parts = file_path.stem.split('-')
    return { 'start': self.file_timestamp_from_formatted_str(parts[0]), 'end': self.file_timestamp_from_formatted_str(parts[1]) }
  
  def file_timestamp_to_formatted_str(self, timestamp: int):
    timestamp = datetime.datetime.utcfromtimestamp(timestamp)
    return timestamp.strftime('%Y%m%d_%H%M%S')
  
  def file_timestamp_from_formatted_str(self, raw: str) -> int:
    return datetime.datetime.strptime(raw, '%Y%m%d_%H%M%S').timestamp()

  async def get_log_start_timestamp(self) -> int:
    """
    Returns the timestamp of the first log file.
    """
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
      self.opened_file = open(filepath, 'a', buffering=1)
      self.opened_file_timestamp = containing_file_timestamp

      return not file_existed

  def get_filepath_for_timestamp(self, start_timestamp):
    end_timestamp = start_timestamp + self.file_interval
    return self.directory/"{}-{}.csv".format(
      self.file_timestamp_to_formatted_str(start_timestamp),
      self.file_timestamp_to_formatted_str(end_timestamp))

  async def get_current_sensor_data(self):
    return await self.sensor_manager.get_latest_values()