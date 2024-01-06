import asyncio
import websockets

async def hello(uri):
  async with websockets.connect(uri) as websocket:
    await websocket.send("Jimmy")
    print(f"(client) send to server: Jimmy")
    name = await websocket.recv()
    print(f"(client) recv from server {name}")

async def rec(uri):
  async with websockets.connect(uri) as websocket:
    while True:
      try:
        word = await websocket.recv()
        print(word)
      except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
        break
    

asyncio.get_event_loop().run_until_complete(
  rec('ws://localhost:8765'))