import asyncio
import websockets
import json

products = [
    {"id": 1, "title": "Product 1", "price": 100},
    {"id": 2, "title": "Product 2", "price": 200},
    {"id": 3, "title": "Product 3", "price": 300},
]

cart = []

async def server(websocket, path):
    await websocket.send(json.dumps({'action': 'load_products', 'products': products}))
    await websocket.send(json.dumps({'action': 'load_cart', 'cart': cart}))

    async for message in websocket:
        data = json.loads(message)
        action = data.get('action')
        if action == 'add_to_cart':
            product_id, product_quantity = int(data.get('id')), int(data.get('quantity'))
            product = next((p for p in products if p['id'] == product_id), None)
            if product:
                cart_item = next((item for item in cart if item['id'] == product_id), None)
                if cart_item:
                    cart_item['quantity'] += product_quantity
                else:
                    product['quantity'] = product_quantity
                    cart.append(product)
                await websocket.send(json.dumps({'action': 'load_cart', 'cart': cart}))

        elif action == 'remove_from_cart':
            product_id = int(data.get('id'))
            cart_item = next((item for item in cart if item['id'] == product_id), None)
            if cart_item:
                cart.remove(cart_item)
                await websocket.send(json.dumps({'action': 'load_cart', 'cart': cart}))

        elif action == 'change_quantity':
            product_id, change = int(data.get('id')), int(data.get('quantity'))
            cart_item = next((item for item in cart if item['id'] == product_id), None)
            if cart_item:
                cart_item['quantity'] += change
                if cart_item['quantity'] <= 0:
                    cart.remove(cart_item)
                await websocket.send(json.dumps({'action': 'load_cart', 'cart': cart}))

start_server = websockets.serve(server, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()