# Python backend for reading, storing and serving sensor data

To run a server with mock data for demonstration or testing purposes use `python main.py --mock`.

<br>

Other available command line options are:

**--sensors**: path to yaml configuration file, not required if --mock is given

**--logger**: path to yaml configuration file, not required if --mock is given

**--host**

**--port**

<br>

Run `python main.py --help` to see the list of available arguments.

<br>

Dependencies listed in requirements.txt.

<br>

# Installation on Raspberry Pi

After cloning the repository go to the backend directory: `cd backend`.

A Python version >= 3.7 is required.

Setup a venv environment: `python3 -m venv venv`.

Activate the environment: `source venv/bin/activate`.

Install core dependencies: `pip install -r requirements_core.txt`.

Install dependencies for reading out sensors: `pip install -r requirements_sensors.txt`.

<br>

# Configuration

Configuration options can be set in yaml files. The paths to these files are provided to the program via the above listed command line options.

<br>

## Sensor configuration

<br>

Three sensor types are supported: mock (generates sine wave), dht22 and ds18b20.  
To add multiple sensors, place multiple configuration blocks as given below in the same file. The dash (-) needs to be written at the beginning of each block.

<br>

### options for type mock
```
- type: mock
  id: <choose an arbitrary unique integer id>
  position: <string describing the position so that the sensor can be identified in the dashboard>
  correction_offset: <a value added to the sensor readout for correction purposes>
  amplitude: <amplitude of generated sine wave>
  mean: <mean of generated sine wave>
  period: <cycle duration in seconds>
```

example
```
- type: mock
  id: 0
  position: "nowhere"
  correction_offset: -2.0
  amplitude: 5
  mean: 20
  period: 30
```