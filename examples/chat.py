import asyncio
import websanic
from sanic.response import html
from websockets.exceptions import ConnectionClosed
import datetime
import random

app = websanic.Sanic()

connections = set()
async def time(websocket, path):
    while True:
        connections.add(websocket)
        mesg = await websocket.recv()
        for connection in connections.copy():
            try:
                await connection.send(mesg)
            except ConnectionClosed:
                connections.remove(connection)


app.websocket(time, 'localhost', 3000)

@app.route('/')
def hello(request):
    return html(open('chat.html').read())

app.run(port=8000)
