import websockets
import asyncio

async def serve(websocket, path):

    print("Connected to", websocket, path)

    await websocket.send("HI!")

start_server = websockets.serve(serve, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()