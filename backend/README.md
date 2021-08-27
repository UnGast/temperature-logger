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

Install dependencies for reading out sensors: `pip install -r requirements_sensors.txt`