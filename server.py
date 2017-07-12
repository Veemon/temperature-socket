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

    _log_path = 'gpu-temps.log'
    _sleep_timer = 5
    _poll_timer = 1

    thread = 0
    slept = False

    def load_data(self):
        with open(self._log_path) as f:
            content = f.readlines()
        return [x.strip() for x in content]

    def poll_data(self):
        try:
            # Sleep For IOLoop Startup
            if not self.slept:
                time.sleep(self._sleep_timer)
                self.slept = True

            # Poll Log File
            #data = 'data'

            # Send Socket Update
            #self.write_message(message=data)

            # Recurse
            threading.Timer(self._poll_timer, self.poll_data).start()
        except:
            pass

    def open(self):
        print("~ socket opened ~")
        for package in self.load_data():
            self.write_message(message=package)
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

if __name__ == "__main__":
    try:
        print('started...')
        app = App().listen(80)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('...stopped')
        tornado.ioloop.IOLoop.instance().stop()
