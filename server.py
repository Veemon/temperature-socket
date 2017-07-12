#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import tornado.websocket

import threading
import time
import os

class Index(tornado.web.RequestHandler):
    def get(self):
        self.render("res/index.html")

class Socket(tornado.websocket.WebSocketHandler):

    _sleep_timer = 5
    _poll_timer = 1

    thread = 0
    slept = False

    def poll_data(self):
        try:
            # Sleep For IOLoop Startup
            if not self.slept:
                time.sleep(self._sleep_timer)
                self.slept = True

            # Poll Log File
            data = 'data'
            print(data)

            # Send Socket Update
            self.write_message(message=data)

            # Recurse
            threading.Timer(self._poll_timer, self.poll_data).start()
        except:
            pass

    def open(self):
        print("~ socket opened ~")
        if self.thread == 0:
            self.thread = threading.Timer(self._poll_timer, self.poll_data)
            self.thread.start()

    def on_close(self):
        print("~ socket closed ~")
        self.thread.cancel()
        self.thread = 0
        self.slept = False

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

# def poll_data(slept):
#     # Sleep For IOLoop Startup
#     if not slept:
#         time.sleep(5)
#
#     # Poll Log File
#     data = 'data'
#     print(data)
#
#     # Send Socket Update
#     tornado.websocket.WebSocketHandler.write_message(message=data)
#
#     # Recurse
#     threading.Timer(1, poll_data, [True]).start()

if __name__ == "__main__":
    try:
        print('started...')
        app = App().listen(80)
        # poll_data(False)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('...stopped')
        tornado.ioloop.IOLoop.instance().stop()
