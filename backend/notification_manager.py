from abc import ABC, abstractmethod
from collections import namedtuple
import asyncio
from threading import Thread
from pathlib import Path
import time
from typing import List, Any, Optional
import yaml
from sensor_manager import SensorManager
from email_manager import EmailManager

class NotificationConfig(ABC):
	def __init__(self, sender_email: str, receiver_email: str, message_subject: str, message: Optional[str]):
		self.sender_email = sender_email
		self.receiver_email = receiver_email
		self.message_subject = message_subject
		self.message = message

	@classmethod
	@abstractmethod
	def get_type_name(cls):
		pass

	@classmethod
	def from_dict(cls, raw_dict):
		cls_params = cls.params_from_dict(raw_dict)

		if cls_params == False:
			raise Exception('raw dictionary does not seem to encode for this message type')
		
		result = cls(
			sender_email=raw_dict['sender'],
			receiver_email=raw_dict['receiver'],
			message_subject=raw_dict['message_subject'],
			message=raw_dict['message'] if 'message' in raw_dict else None,
			**cls_params)

		return result

	@classmethod
	@abstractmethod
	def params_from_dict(cls, raw_dict):
		pass

	@abstractmethod
	def check_signal(self, current_sensor_values) -> bool:
		pass

class BaseThresholdNotificationConfig(NotificationConfig):
	def __init__(self, sensor_id: str, threshold: float, check_interval: float, **kwargs):
		super().__init__(**kwargs)
		self.sensor_id = sensor_id
		self.threshold = threshold
		self.check_interval = check_interval
		self.previous_check_value = None

	@classmethod
	@abstractmethod
	def get_type_name(cls):
		pass

	@classmethod
	def params_from_dict(cls, raw_dict):
		threshold = next(value for key, value in raw_dict.items() if key == cls.get_type_name())

		if threshold is None:
			return False
		
		threshold = float(threshold)
		
		return {
			'sensor_id': raw_dict['sensor'],
			'threshold': threshold,
			'check_interval': float(raw_dict['check_interval'])
		}

	@abstractmethod
	def check_signal(self, current_value, previous_value) -> bool:
		pass

	def __str__(self):
		return f'Notification {{ {self.get_type_name()}: {str(self.threshold)}, sender: {self.sender_email}, receiver: {self.receiver_email} }}'

class FallBelowNotificationConfig(BaseThresholdNotificationConfig):
	@classmethod
	def get_type_name(cls):
		return 'fall_below'
	
	def check_signal(self, current_sensor_values) -> bool:
		current_value = current_sensor_values[self.sensor_id]

		result = False

		if self.previous_check_value is not None:
			result = self.threshold > current_value and self.previous_check_value > self.threshold

		self.previous_check_value = current_value

		return result

class RiseAboveNotificationConfig(BaseThresholdNotificationConfig):
	@classmethod
	def get_type_name(cls):
		return 'rise_above'

	def check_signal(self, current_sensor_values) -> bool:
		current_value = current_sensor_values[self.sensor_id]

		result = False

		if self.previous_check_value is not None:
			result = self.threshold < current_value and self.previous_check_value < self.threshold

		self.previous_check_value = current_value

		return result

class SystemStartNotificationConfig(NotificationConfig):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.checked_once = False

	@classmethod
	def params_from_dict(cls, raw_dict):
		return {}

	def check_signal(self, current_sensor_values) -> bool:
		result = not self.checked_once
		self.checked_once = True
		return result

class NotificationManager:
	def __init__(self, notification_configs, sensor_manager: SensorManager, email_manager: EmailManager):
		self.notification_configs = notification_configs
		self.sensor_manager = sensor_manager
		self.email_manager = email_manager
		self.last_check_timestamps = {}
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

					try:
						if notification_config.check_signal(self.current_sensor_values):
							self.send_notification(notification_config)
					except Exception as e:
						print(f'an error occurred while attempting to check or send notification {notification_config}', e)
		finally:
				time.sleep(1)
				self.watch_loop()

	def send_notification(self, notification_config: NotificationConfig):
		print('send notification for config:', notification_config)
		
		text = notification_config.message
		if text is None:
			text = 'notification was automatically sent'

		self.email_manager.send_email(
			sender_address=notification_config.sender_email,
			receiver_address=notification_config.receiver_email,
			subject=notification_config.message_subject,
			text=text)
	
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
					raise Exception(f'found no matching type for notification config at index: {index}')
					
			return notification_configs