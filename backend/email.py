import smtplib
from email.mime.text import MIMEText
from pathlib import Path
import yaml
from typing import List 

class EmailAddressConfig:
	def __init__(self, address: str, password: str, smtp_host: str, smtp_port: int):
		self.address = address
		self.password = password
		self.smtp_host = smtp_host
		self.smtp_port = smtp_port

class EmailManager:
	def __init__(self, address_configs: List[EmailAddressConfig]):
		self.address_configs = address_configs
	
	def get_address_config(self, address: str) -> EmailAddressConfig:
		for config in self.address_configs:
			if config.address == address:
				return config
		
		raise Exception(f'no config found for address "{address}"')
	
	def send_email(self, sender_address: str, receiver_address: str, subject: str, text: str):
		sender_address_config = self.get_address_config(sender_address)

		smtp_client = smtplib.SMTP(host=sender_address_config.smtp_host, port=sender_address_config.smtp_port)
		smtp_client.starttls()
		smtp_client.login(sender_address_config.address, sender_address_config.password)

		message = MIMEText(subject)
		message['From'] = sender_address_config.address
		message['To'] = receiver_address
		message['Subject'] = text

		smtp_client.send_message(message)

	@staticmethod
	def parse_config(config_file_path: Path) -> List[EmailAddressConfig]:
		with open(config_file_path, 'rb') as file:
			config = yaml.load(file, Loader=yaml.Loader)

			