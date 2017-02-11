from sanic import Sanic
import websockets
import asyncio

class Sanic(Sanic):
    def __init__(self):
        super().__init__()
        self.before_start = None

    def websocket(self, handler, host='localhost', port='3000'):
        server = websockets.serve(handler, host, port)

        def before_start(app, loop):
            asyncio.get_event_loop().run_until_complete(server)
        self.before_start = before_start

    def run(self, *args, **kwargs):
        before_start = kwargs.get('before_start')
        if self.before_start is not None:
            _before_start = before_start

            def _before(app, loop):
                if _before_start is not None:
                    _before_start(app, loop)
                self.before_start(app, loop)
            before_start = _before
        kwargs['before_start'] = before_start
        super().run(*args, **kwargs)
