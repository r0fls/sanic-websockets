# sanic-websockets
sanic + websockets

Small wrapper to make running a [websockets](http://websockets.readthedocs.io/en/stable/intro.html) server from the same app easier.

Note this is no longer needed because native sanic websocket support has been added ~has already become less useful because I added a method `add_task` to sanic that allows integrating with other servers like websockets fairly easy. See the PR here for more context: https://github.com/channelcat/sanic/pull/411~.

**ws.py**
```python

import asyncio
import websanic
from sanic.response import html
import datetime
import random

app = websanic.Sanic()

async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)

app.websocket(time, 'localhost', 3000)

@app.route('/')
def hello(request):
    return html(open('ws.html').read())

app.run(port=8000)
```

**ws.html**
```html
<!DOCTYPE html>
<html>
  <head>
    <title>WebSocket demo</title>
  </head>
  <body>
    <script>
      var ws = new WebSocket("ws://127.0.0.1:3000/"),
        messages = document.createElement('ul');
      ws.onmessage = function (event) {
        var messages = document.getElementsByTagName('ul')[0],
          message = document.createElement('li'),
          content = document.createTextNode(event.data);
        message.appendChild(content);
        messages.appendChild(message);
      };
      document.body.appendChild(messages);
    </script>
  </body>
</html>
```
