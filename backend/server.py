import websockets
import asyncio
import json
import DataSource

class WebsocketProtocol:


    def __init__(self, socket, data_source):

        self.streaming = False

        self.socket = socket

        self.data_source = data_source

        self.listen_task = asyncio.create_task(self.listen())


    async def execute(self):

        await self.listen_task


    async def listen(self):

        print("Start listening on socket", self.socket)

        while True:

            try:
            
                message = await self.socket.recv()
        
                await self.onmessage(message)

            except:

                break


    async def onmessage(self, message):

        print("Received message", message)

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

        else:

            self.end_protocol_violation("unsupported action requested")


    async def end_protocol_violation(self, description):

        await self.socket.send("Ending communication because of protocol violation: {}".format(description))

        await self.socket.close()


    async def stream_values(self, interval):

        try:

            self.streaming = True

            while True:

                if not self.streaming:
                    
                    break

                await self.socket.send(json.dumps({
                    "type": "stream_value",
                    "values": self.data_source.get_latest_values()
                }))

                await asyncio.sleep(interval)
        
        finally:

            self.streaming = False

            print("Stopped streaming values.")

    async def send_sensor_info(self):

        print("SEND SENSOR INFO")

        await self.socket.send(json.dumps({
            "type": "sensor_info",
            "sensors": [s.__dict__ for s in self.data_source.get_sensors()]
        }))


async def serve(websocket, path):

    print("Connected to", websocket, path)

    protocol = WebsocketProtocol(websocket, DataSource.MockDataSource())

    await protocol.execute()



start_server = websockets.serve(serve, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()