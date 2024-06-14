import asyncio
import websockets
import json


cart = []


async def server(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        if data['action'] == 'add_to_cart':
            cart.append(data['item'])
            await websocket.send(json.dumps({'action': 'update_cart', 'items': cart}))


start_server = websockets.serve(server, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()