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

<br>

```
- type: mock
  id: <choose an arbitrary unique integer id>
  position: "<string describing the position so that the sensor can be identified on the dashboard>"
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

<br>

### options for type dht22

<br>

```
- type: dht22
  id: <choose an arbitrary unique integer id>
  position: "<string describing the position so that the sensor can be identified on the dashboard>"
  pin: "<GPIO pin number prefixed with "D", for example D17 for GPIO pin 17>"
  correction_offset: <a value added to the sensor readout for correction purposes>
```

example
```
- type: dht22
  id: 0
  position: "position"
  pin: "D4"
  correction_offset: 0
```

<br>

### options for type ds18b20

<br>

```
- type: ds18b20
  id: <choose an arbitrary unique integer id>
  position: "<string describing the position so that the sensor can be identified on the dashboard>"
  device_id: "<the unique id of the sensor in the one wire protocol>"
  correction_offset: <a value added to the sensor readout for correction purposes>
```

example

```
- type: ds18b20
  id: 0
  position: "position"
  device_id: "28-0300a279abec"
  correction_offset: 0
```

<br>

## Logger

<br>

### Mock Logger

Does not output to a file, only to the console.

```
type: mock
interval: <interval between console outputs>
```

<br>

### Default Logger

Writes data in CSV format into files named by date in the specified directory.

```
type: default
interval: <interval between writes to files>
directory: <absolute path to directory where data files should be placed>
```

<br>

## Emails

<br>

Configuration for emails used to send notifications. To provide multiple emails, put multiple blocks of the following syntax in the configuration file. The dash (-) at the beginning of each block is mandatory.

<br>

```
- address: <the email address>
  name: '<the name displayed as sender of notifications>'
  host: <smtp host address>
  port: <smtp port>
  password: '<password for the email address>'
```