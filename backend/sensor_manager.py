from abc import ABC, abstractmethod

class SensorManager(ABC):
	def __init__(self, sensors):
		self.sensors = sensors
		self.last_read_not_none_values = {}

	async def get_latest_values_with_invalids(self):
		"""invalid values/failed reads are output as None and not replaced with 0"""
		values = {}

		for sensor in self.sensors:
			try:
				values[sensor.id] = sensor.read()
            
			except Exception as e:
				print("could not read value for sensor", sensor, e)
				values[sensor.id] = None
			
		return values

	async def get_latest_values_filled_with_previous(self):
		"""replaces failed reads with values from previous non-failed reads, keeps None if no previous value is
		available"""
		current_values = await self.get_latest_values_with_invalids()
		filled_values = current_values
		for key, value in filled_values.items():
			if value is None and key in self.last_read_not_none_values:
				filled_values[key] = self.last_read_not_none_values[key]
			elif value is None and key not in self.last_read_not_none_values:
				filled_values[key] = None
			elif value is not None:
				self.last_read_not_none_values[key] = value
		return filled_values

	async def get_latest_values(self):
		"""replaces failed reads with values from previous non-failed reads or 0 if no previous value is available"""
		values = await self.get_latest_values_filled_with_previous()
		for key, value in values.items():
			if value is None:
				values[key] = 0

		return values
