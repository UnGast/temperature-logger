import math
import asyncio
import io 
import time
from .DataLogger import DataLogger

class MockDataLogger(DataLogger):
  async def log_loop(self):
    while True:
      print("would log data if it wasn't a mock")
      await asyncio.sleep(self.interval)

  async def get_past_data(self, start: int, end: int):
    data = []

    for i in range(start, end, 10):
      data_entry = { 'timestamp_unix': i, 'timestamp_human': self.format_unix_timestamp(i) }

      for sensor in self.sensor_manager.sensors:
        data_entry[sensor.id] = math.sin(i)

      data.append(data_entry)
      
    return data

  async def get_log_files_containing_interval(self, start: int, end: int):
    return await self.get_log_files()

  async def get_log_files(self):
    file = io.StringIO()
    file.name = 'testfile'
    file.writelines([
      self.csv_file_manager.get_csv_header() + '\n',
      await self.make_sensor_values_csv_line(int(time.time()), await self.sensor_manager.get_latest_values())
    ])
    file.seek(0)
    return [file]