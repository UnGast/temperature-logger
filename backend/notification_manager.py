from abc import ABC, abstractmethod
from collections import namedtuple
import asyncio
from threading import Thread
from pathlib import Path
import time
from typing import List, Any
import yaml
from sensor_manager import SensorManager
from email_manager import EmailManager

class NotificationConfig(ABC):
	def __init__(self, sensor_id: str, threshold: float, sender_email: str, receiver_email: str, check_interval: float, message_subject: str):
		self.sensor_id = sensor_id
		self.threshold = threshold
		self.sender_email = sender_email
		self.receiver_email = receiver_email
		self.check_interval = check_interval
		self.message_subject = message_subject
	
	@classmethod
	@abstractmethod
	def get_type_name(cls):
		pass

	@classmethod
	def from_dict(cls, raw_dict):
		threshold = next(value for key, value in raw_dict.items() if key == cls.get_type_name())

		if threshold is None:
			return None
		
		threshold = float(threshold)
		
		return cls(
			sensor_id=raw_dict['sensor'],
			threshold=threshold,
			sender_email=raw_dict['sender'],
			receiver_email=raw_dict['receiver'],
			check_interval=float(raw_dict['check_interval']),
			message_subject=raw_dict['message_subject']
		)

	@abstractmethod
	def check_signal(self, current_value, previous_value) -> bool:
		pass

	def __str__(self):
		return f'Notification {{ {self.get_type_name()}: {str(self.threshold)}, sender: {self.sender_email}, receiver: {self.receiver_email} }}'

class FallBelowNotificationConfig(NotificationConfig):
	@classmethod
	def get_type_name(cls):
		return 'fall_below'
	
	def check_signal(self, current_value, previous_value) -> bool:
		return self.threshold > current_value and previous_value > self.threshold

class RiseAboveNotificationConfig(NotificationConfig):
	@classmethod
	def get_type_name(cls):
		return 'rise_above'

	def check_signal(self, current_value, previous_value) -> bool:
		return self.threshold < current_value and previous_value < self.threshold

class NotificationManager:
	def __init__(self, notification_configs, sensor_manager: SensorManager, email_manager: EmailManager):
		self.notification_configs = notification_configs
		self.sensor_manager = sensor_manager
		self.email_manager = email_manager
		self.last_check_timestamps = {}
		self.previous_check_values = {}
		self.current_sensor_values = None
	
	def start_watching(self):
		thread = Thread(target=self.watch_loop)
		thread.start()
	
	def watch_loop(self):
		current_timestamp = time.time()

		self.current_sensor_values = asyncio.run(self.sensor_manager.get_latest_values())

		try:
			for index, notification_config in enumerate(self.notification_configs):
				if not index in self.last_check_timestamps or\
					self.last_check_timestamps[index] + notification_config.check_interval <= current_timestamp:
					
					self.last_check_timestamps[index] = current_timestamp
					current_check_value = self.current_sensor_values[notification_config.sensor_id]

					if index in self.previous_check_values:
						try:
							if notification_config.check_signal(
								self.current_sensor_values[notification_config.sensor_id],
								self.previous_check_values[index]):
								self.send_notification(notification_config)
						except Exception as e:
							print(f'an error occurred while attempting to check or send notification {notification_config}', e)

					self.previous_check_values[index] = current_check_value
		finally:
			time.sleep(1)
			self.watch_loop()

	def send_notification(self, notification_config: NotificationConfig):
		print('send notification for config:', notification_config)
		self.email_manager.send_email(
			sender_address=notification_config.sender_email,
			receiver_address=notification_config.receiver_email,
			subject=notification_config.message_subject,
			text='notification was automatically sent')
	
	@staticmethod
	def parse_notifications_config(config_file_path: Path) -> List[Any]:
		with open(config_file_path, 'rb') as file:
			raw_notification_configs = yaml.load(file, Loader=yaml.Loader)

			potential_config_types = [FallBelowNotificationConfig, RiseAboveNotificationConfig]
			notification_configs = []
			for index, raw_notification_config in enumerate(raw_notification_configs):
				found_matching_type = False

				for potential_type in potential_config_types:
					try:
						parsed = potential_type.from_dict(raw_notification_config)
						if parsed is not None:
							notification_configs.append(parsed)
							found_matching_type = True
							break	
					except Exception as e:
						#print(f'error when parsing config {index}: {e}')
						pass

				if not found_matching_type:
					raise Exception('found no matching type for notification config at index: {index}')
					
			return notification_configs