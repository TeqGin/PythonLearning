import asyncio
import threading
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

def serve():
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(
    websockets.serve(srv, 'localhost', 8765)
  )
  loop.run_forever()

t1 = threading.Thread(target=serve)
t1.start()
t1.join()