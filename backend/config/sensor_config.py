import sensors
import yaml

def parse(file_path) -> [sensors.Sensor]:

  print("parsing sensor configuration file at: {}".format(file_path))

  config = None

  sensor_instances: [sensors.Sensor] = []

  try:

    with open(file_path, 'rb') as file:

      config = yaml.load(file, Loader=yaml.Loader)

    print("got config: {}".format(config))

    for sensor_config in config:

      type_key = sensor_config['type'].lower()

      for sensor_type in dir(sensors):

        if sensor_type.lower() == type_key:

          SensorClass = getattr(sensors, sensor_type)

          sensor_arguments = { k: v for k, v in sensor_config.items() if k != "type" }

          sensor_instance = SensorClass(**sensor_arguments)

          sensor_instances.append(sensor_instance)

  except Exception as e:

    print("there seems to be an error with the provided configuration file, error: {}".format(e))

  print("sensors initialized: {}".format(len(sensor_instances)))

  return sensor_instances

if __name__ == "__main__":
    
  import sys
  from pathlib import Path

  parse(Path.cwd()/sys.argv[1])