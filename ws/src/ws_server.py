import asyncio
import websockets

async def echo(websocket, path):
  async for message in websocket:
    print(message,'received from client')
    greeting = f"Hello {message}!"
    await websocket.send(greeting)
    print(f"> {greeting}")

async def srv(websocket, path):
  for s in ["hello", "world","my","name","is","ross"]:
    print(s)
    await websocket.send(s)

asyncio.get_event_loop().run_until_complete(
  websockets.serve(srv, 'localhost', 8765))
asyncio.get_event_loop().run_forever()