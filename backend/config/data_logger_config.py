import yaml
import data_logger

def parse(config_file_path) -> (any, dict):

  print("parsing data logger config file at: {}".format(config_file_path))

  try:

    config = None

    with open(config_file_path, 'rb') as file:

      config = yaml.load(file, Loader=yaml.Loader)

    print("got config:", config)

    type_key = config["type"].lower()

    data_logger_key = None

    for module_key in dir(data_logger):

      if module_key.lower() == type_key:

        data_logger_key = module_key

    if data_logger_key is None:

      raise Exception("data logger of type \"{}\" does not exist".format(config["type"]))

    print("found data loader of type:", data_logger_key)

    DataLoggerClass = getattr(data_logger, data_logger_key)

    data_logger_arguments =  { k: v for k, v in config.items() if k != "type" }

    return (DataLoggerClass, data_logger_arguments)

  except Exception as e:

    print("there appears to be a problem with the data logger config file, error:", e)

if __name__ == "__main__":

  import sys

  parse(sys.argv[1])