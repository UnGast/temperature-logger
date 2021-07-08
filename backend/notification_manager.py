from collections import namedtuple
import asyncio
from threading import Thread
from pathlib import Path
import time
from typing import List, Any
import yaml
from sensor_manager import SensorManager

class FallBelowNotificationConfig:
	def __init__(self, sensor_id: str, threshold: float, sender_email: str, receiver_email: str, check_interval: float, message_subject: str):
		self.type = 'fall_below'
		self.sensor_id = sensor_id
		self.threshold = threshold
		self.sender_email = sender_email
		self.receiver_email = receiver_email
		self.check_interval = check_interval
		self.message_subject = message_subject

class NotificationManager:
	def __init__(self, notification_configs, sensor_manager: SensorManager):
		self.notification_configs = notification_configs
		self.sensor_manager = sensor_manager
		self.last_check_timestamps = {}
		self.previous_check_values = {}
		self.current_sensor_values = None
	
	def start_watching(self):
		thread = Thread(target=self.watch_loop)
		thread.start()
	
	def watch_loop(self):
		current_timestamp = time.time()

		self.current_sensor_values = asyncio.run(self.sensor_manager.get_latest_values())

		for index, notification_config in enumerate(self.notification_configs):
			if not index in self.last_check_timestamps or\
				self.last_check_timestamps[index] + notification_config.check_interval <= current_timestamp:
				
				self.last_check_timestamps[index] = current_timestamp
				current_check_value = self.current_sensor_values[notification_config.sensor_id]

				if index in self.previous_check_values:
					if isinstance(notification_config, FallBelowNotificationConfig):
						self.process_fall_config(notification_config, index)

				self.previous_check_values[index] = current_check_value
			
		time.sleep(1)
		self.watch_loop()
	
	def process_fall_config(self, config: FallBelowNotificationConfig, index: int):
		if config.threshold > self.current_sensor_values[config.sensor_id] and self.previous_check_values[index] > config.threshold:
			print('FALL NOTIFICATION')
	
	@staticmethod
	def parse_notifications_config(config_file_path: Path) -> List[Any]:
		with open(config_file_path, 'rb') as file:
			raw_notification_configs = yaml.load(file, Loader=yaml.Loader)

			notification_configs = []
			for index, raw_notification_config in enumerate(raw_notification_configs):
				try:
					parsed = NotificationManager.try_parse_fall_below_config(raw_notification_config)
					if parsed is not None:
						notification_configs.append(parsed)
						continue
				except Exception as e:
					print(f'error when parsing config {index}', e)
				
			return notification_configs

	@staticmethod
	def try_parse_fall_below_config(raw_config) -> FallBelowNotificationConfig:
		threshold = next(value for key, value in raw_config.items() if key == 'fall_below')

		if threshold is None:
			return None
		
		threshold = float(threshold)
		
		return FallBelowNotificationConfig(
			sensor_id=raw_config['sensor'],
			threshold=threshold,
			sender_email=raw_config['sender'],
			receiver_email=raw_config['receiver'],
			check_interval=float(raw_config['check_interval']),
			message_subject=raw_config['message_subject']
		)