from sanic import Sanic
import websockets
import asyncio

class Sanic(Sanic):
    def __init__(self):
        super().__init__()
        self.before_start = None

    def websocket(self, handler, host=None, port=None,
                  *args, **kwargs):
        if kwargs.get('host') is None:
            kwargs['host'] = 'localhost'
        if kwargs.get('port') is None:
            kwargs['port'] = '3000'
        server = websockets.serve(handler, *args, **kwargs)

        @self.listener('before_server_start')
        def before_start(app, loop):
            asyncio.get_event_loop().run_until_complete(server)
