import websockets
import asyncio
import io
import json
import time
from sensor_manager import SensorManager
from data_logger import DataLogger
from notification_manager import NotificationManager
import shutil

class WebsocketProtocol:
    def __init__(self, socket, sensor_manager: SensorManager, data_logger: DataLogger, notification_manager: NotificationManager):
        self.streaming = False
        self.socket = socket
        self.sensor_manager = sensor_manager
        self.data_logger = data_logger
        self.notification_manager = notification_manager
        self.listen_task = asyncio.create_task(self.listen())
        self.listen_task.add_done_callback(self.handle_listen_done)
    
    async def execute(self):
        await self.listen_task

    def handle_listen_done(self, task: asyncio.Task):
        try:
            task.result()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print("Exception in listen", e)

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

            def handle_stream_end(task):
                try:
                    stream_task.result()
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    print("Exception during stream values", e)

            stream_task.add_done_callback(handle_stream_end)

        elif action == "end_stream":
            self.streaming = False

        elif action == "get_sensor_info":
            await self.send_sensor_info()

        elif action == "get_notification_configs":
            await self.send_notification_configs()

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
    
    async def send_notification_configs(self):
        print("sending notification configs")

        prepared_configs = []
        for config in self.notification_manager.notification_configs:
            prepared_config = {
                "type": config.get_type_name()
            }
            if hasattr(config, 'threshold'):
                prepared_config['threshold'] = config.threshold
            prepared_configs.append(prepared_config)

        await self.socket.send(json.dumps({
            "type": "notification_configs",
            "configs": prepared_configs
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
    def __init__(self, sensor_manager: SensorManager, data_logger: DataLogger, notification_manager: NotificationManager):
        self.sensor_manager = sensor_manager
        self.data_logger = data_logger
        self.notification_manager = notification_manager

    async def serve_connection(self, websocket, path):
        print("connected to", websocket, path)
        protocol = WebsocketProtocol(websocket, self.sensor_manager, self.data_logger, self.notification_manager)
        await protocol.execute()

    async def serve(self, host="0.0.0.0", port=8000):
        print("starting server on {}:{}".format(host, port))
        await websockets.serve(self.serve_connection, host=host, port=port)