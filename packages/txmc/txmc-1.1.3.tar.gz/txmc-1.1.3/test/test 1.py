#!/usr/bin/python3
 
import websockets
import asyncio
 
async def hello(websocket,path):
		name = await websocket.recv()
		print(f"A new client : {name}")
		greeting = "Welcome " + name
		await websocket.send(greeting)
		print(f"send '{greeting}' to '{name}'")
		
start_server = websockets.serve(hello,'0.0.0.0',8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()