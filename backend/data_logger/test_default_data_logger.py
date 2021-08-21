from .DefaultDataLogger import DefaultDataLogger

class MockSensorManager:
	def __init__(self):
		self.sensors = {}

def test_data_file_name():
	logger = DefaultDataLogger(sensor_manager=MockSensorManager(), interval=1, file_interval=1, directory="")
	assert logger.get_filepath_for_timestamp(0) is not None