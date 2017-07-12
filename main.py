import tornado.ioloop
import tornado.web
import tornado.websocket

import os

class Index(tornado.web.RequestHandler):
    def get(self):
        self.render("res/index.html")

class Socket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", Index),
            (r"/ws", Socket),
        ]
        settings = {
            "static_path": os.path.abspath('./res/')
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    try:
        print('started...')
        app = App().listen(80)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('...stopped')
        tornado.ioloop.IOLoop.instance().stop()
