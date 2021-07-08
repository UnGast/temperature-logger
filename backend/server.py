import websockets
import asyncio
import io
import json
import time
from sensor_manager import SensorManager
from data_logger import DataLogger
import shutil

class WebsocketProtocol:
    def __init__(self, socket, sensor_manager: SensorManager, data_logger: DataLogger):
        self.streaming = False
        self.socket = socket
        self.sensor_manager = sensor_manager
        self.data_logger = data_logger
        self.listen_task = asyncio.create_task(self.listen())

    async def execute(self):
        await self.listen_task

    async def listen(self):
        print("starting listening on socket", self.socket)
        while True:
            try:
                message = await self.socket.recv()
                await self.onmessage(message)
            except Exception as e:
                print("an error occurred while handling a message", e)
                break

    async def onmessage(self, message):
        print("received message", message)
        payload = json.loads(message)
        action = payload["action"]

        if action == "stream":
            interval = int(payload["interval"])
            if interval < 1:
                await self.end_protocol_violation("streaming interval must be at least 1 second")
            stream_task = asyncio.create_task(self.stream_values(interval))

        elif action == "end_stream":
            self.streaming = False

        elif action == "get_sensor_info":
            await self.send_sensor_info()

        elif action == "get_past_data":
          start = int(payload["start"])
          end = int(payload["end"])
          await self.send_past_data(start, end)

        elif action == "get_log_files_containing_interval":
            start = int(payload["start"])
            end = int(payload["end"])
            await self.send_log_files_containing_interval(start, end)

        elif action == "get_all_log_files":
            await self.send_all_log_files()
        
        elif action == "get_server_meta":
            await self.send_server_meta()

        else:
            self.end_protocol_violation("unsupported action requested")

    async def end_protocol_violation(self, description):
        await self.socket.send("ending communication because of protocol violation: {}".format(description))
        await self.socket.close()

    async def stream_values(self, interval):
        try:
            self.streaming = True
            while True:
                if not self.streaming:
                    break

                await self.socket.send(json.dumps({
                    "type": "stream_value",
                    "timestamp": int(time.time()),
                    "values": await self.sensor_manager.get_latest_values()
                }))

                await asyncio.sleep(interval)

        finally:
            self.streaming = False
            print("stopped streaming values")

    async def send_sensor_info(self):
        print("sending sensor info")
        await self.socket.send(json.dumps({
            "type": "sensor_info",
            "sensors": [s.get_info() for s in self.sensor_manager.sensors]
        }))

    async def send_past_data(self, start: int, end: int):
        print("sending past data from {} to {}".format(start, end))
        data = await self.data_logger.get_past_data(start, end)
        await self.socket.send(json.dumps({
          "type": "past_data",
          "data": data
        }))

    async def send_log_files_containing_interval(self, start: int, end: int):
        files = await self.data_logger.get_log_files_containing_interval(start, end)
        for file_or_path in files:
            try:
                file = None
                if isinstance(file_or_path, io.IOBase):
                    file = file_or_path
                else:
                    file = open(file_or_path, 'r')
                await self.socket.send(json.dumps({
                    "type": "log_file",
                    "contents": file.read(),
                    "filename": file.name
                }))

            finally:
                file.close()

    async def send_all_log_files(self):
        files = await self.data_logger.get_log_files()
        for file_or_path in files:
            try:
                file = None
                if isinstance(file_or_path, io.IOBase):
                    file = file_or_path
                else:
                    file = open(file_or_path, 'r')
                await self.socket.send(json.dumps({
                    "type": "log_file",
                    "contents": file.read(),
                    "filename": file.name
                }))

            finally:
                file.close()

    async def send_server_meta(self):
        total, used, free = shutil.disk_usage("/")
        
        await self.socket.send(json.dumps({
            "type": "server_meta",
            "meta": {
                "disc": {
                    "total": total,
                    "used": used,
                    "free": free
                }
            }
        }))

class Server:
    def __init__(self, sensor_manager: SensorManager, data_logger: DataLogger):
        self.sensor_manager = sensor_manager
        self.data_logger = data_logger

    async def serve_connection(self, websocket, path):
        print("connected to", websocket, path)
        protocol = WebsocketProtocol(websocket, self.sensor_manager, self.data_logger)
        await protocol.execute()

    async def serve(self, host="0.0.0.0", port=8000):
        print("starting server on {}:{}".format(host, port))
        async with websockets.serve(self.serve_connection, host="localhost", port=port):
            await asyncio.Future()