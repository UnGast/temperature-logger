import argparse
import asyncio
from pathlib import Path
import data_logger
from sensor_manager import SensorManager
from server import Server
from email_manager import EmailManager
from notification_manager import NotificationManager
import config

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--mock", action="store_true", help="serve data that is generated for testing purposes, if given --sensors and --logger are not required")
arg_parser.add_argument("--sensors", help="a yaml file that defines a list of sensors")
arg_parser.add_argument("--logger", help="a yaml file that defines the configuration for the data logger")
arg_parser.add_argument("--emails", help="a yaml file that defines configuration for email addresses")
arg_parser.add_argument("--notifications", help="a yaml file that defines configuration for notifications")
arg_parser.add_argument("--host", help="which host should the server listen on", default="0.0.0.0")
arg_parser.add_argument("--port", help="which port should the server bind to", default=8000)
args = arg_parser.parse_args()

sensor_config_file_path = None
data_logger_config_file_path = None
emails_config_file_path = None
notifications_config_file_path = None

if args.mock:
    sensor_config_file_path = Path.cwd()/"config/mock_sensors.yaml"
    data_logger_config_file_path = Path.cwd()/"config/mock_data_logger.yaml"
    emails_config_file_path = Path.cwd()/"config/mock_emails.yaml"
    notifications_config_file_path = Path.cwd()/"config/mock_notifications.yaml"
else:
    sensor_config_file_path = args.sensors
    data_logger_config_file_path = args.logger
    emails_config_file_path = args.emails
    notifications_config_file_path = args.notifications

if sensor_config_file_path is None:
    raise Exception("no sensors config file given")

if data_logger_config_file_path is None:
    raise Exception("no data logger config file given")

if emails_config_file_path is None:
    raise Exception("no emails config file given")

if notifications_config_file_path is None:
    raise Exception("no notifications config file given")
 
sensors = config.parse_sensor_config(sensor_config_file_path)
sensor_manager = SensorManager(sensors)

(DataLoggerClass, data_logger_arguments) = config.parse_data_logger_config(data_logger_config_file_path)
data_logger = DataLoggerClass(sensor_manager=sensor_manager, **data_logger_arguments)

email_manager = EmailManager(address_configs=EmailManager.parse_address_configs(emails_config_file_path))

notification_manager = NotificationManager(notification_configs=NotificationManager.parse_notifications_config(config_file_path=notifications_config_file_path), sensor_manager=sensor_manager, email_manager=email_manager)
notification_manager.start_watching()

print("initialized application with sensors:", sensors, "and data logger", data_logger)

server = Server(sensor_manager, data_logger, notification_manager)
asyncio.gather(server.serve(host=args.host, port=args.port), data_logger.log_loop())
asyncio.get_event_loop().run_forever()