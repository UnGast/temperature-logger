import argparse
import asyncio
from pathlib import Path
import data_logger
from SensorManager import SensorManager
from Server import Server
import config

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--mock", action="store_true", help="serve data that is generated for testing purposes, if given --sensors and --logger are not required")
arg_parser.add_argument("--sensors", help="a yaml file that defines a list of sensors")
arg_parser.add_argument("--logger", help="a yaml file that defines the configuration for the data logger")
arg_parser.add_argument("--host", help="which host should the server listen on", default="0.0.0.0")
arg_parser.add_argument("--port", help="which port should the server bind to", default=8000)
args = arg_parser.parse_args()

sensor_config_file_path = None
data_logger_config_file_path = None

if args.mock:
    sensor_config_file_path = Path.cwd()/"config/mock_sensors.yaml"
    data_logger_config_file_path = Path.cwd()/"config/mock_data_logger.yaml"
else:
    sensor_config_file_path = args.sensors
    data_logger_config_file_path = args.logger

if sensor_config_file_path is None:
    raise Exception("no sensors config file given")

if data_logger_config_file_path is None:
    raise Exception("no data logger config file given")
 
sensors = config.parse_sensor_config(sensor_config_file_path)
sensor_manager = SensorManager(sensors)

(DataLoggerClass, data_logger_arguments) = config.parse_data_logger_config(data_logger_config_file_path)
data_logger = DataLoggerClass(sensor_manager=sensor_manager, **data_logger_arguments)

print("initialized application with sensors:", sensors, "and data logger", data_logger)

server = Server(sensor_manager, data_logger)
asyncio.gather(server.serve(host=args.host, port=args.port), data_logger.log_loop())
asyncio.get_event_loop().run_forever()