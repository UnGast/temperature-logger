import smtplib
from email.mime.text import MIMEText
from pathlib import Path
import yaml
from typing import List 

class EmailAddressConfig:
	def __init__(self, address: str, name: str, password: str, smtp_host: str, smtp_port: int):
		self.address = address
		self.name = name
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

		message = MIMEText(text)
		message['From'] = f'{sender_address_config.name}'
		message['To'] = receiver_address
		message['Subject'] = subject 

		smtp_client.send_message(message)

	@staticmethod
	def parse_address_configs(config_file_path: Path) -> List[EmailAddressConfig]:
		with open(config_file_path, 'rb') as file:
			config = yaml.load(file, Loader=yaml.Loader)

			address_configs = []
			for config_index, raw_address_config in enumerate(config):
				address = raw_address_config['address']
				if address is None:
					print(f'error in email config: address missing (config {config_index})')
					continue

				name = raw_address_config['name']
				if address is None:
					print(f'error in email config: name missing (config {config_index})')
					continue

				password = raw_address_config['password']
				if password is None:
					print(f'error in email config: password missing (config {config_index})')
					continue

				host = raw_address_config['host']
				if host is None:
					print(f'error in email config: host missing (config {config_index})')
					continue

				port = raw_address_config['port']
				if port is None:
					print(f'error in email config: port missing (config {config_index})')
					continue

				address_configs.append(EmailAddressConfig(
					address=address,
					name=name,
					password=password,
					smtp_host=host,
					smtp_port=port
				))
			
			return address_configs

			