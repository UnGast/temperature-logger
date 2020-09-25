import argparse
from pathlib import Path
from SensorManager import SensorManager
from Server import Server
import config

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--mock", action="store_true", help="serve data that is generated for testing purposes")
arg_parser.add_argument("--sensors", help="a yaml file that defines a list of sensors")
args = arg_parser.parse_args()

sensor_config_file_path = None

if args.mock:

    sensor_config_file_path = Path.cwd()/"config/mock_sensors.yaml"

else:

    sensor_config_file_path = args.sensors
 
sensors = config.parse_sensor_config(sensor_config_file_path)

print("initialized application with sensors:", sensors)

sensor_manager = SensorManager(sensors)

server = Server(sensor_manager)

server.serve()