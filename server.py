#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import tornado.websocket

from datetime import datetime
import threading
import time
import os

def get_date(string):
    args = list(map(int, string.split(',')[0].split('-')))
    return datetime(args[-1], args[-2], args[-3], args[-4], args[-5])

class Index(tornado.web.RequestHandler):
    def get(self):
        self.render("res/index.html")

class Socket(tornado.websocket.WebSocketHandler):

    _log_path = 'gpu-temps.log'
    _sleep_timer = 5
    _poll_timer = 5

    thread = 0
    slept = False
    last_point = ['null', '']

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
            loaded_data = self.load_data()
            if loaded_data[-1] != self.last_point:
                d0 = get_date(loaded_data[0])
                d1 = get_date(self.last_point)
                d_ = d1 - d0
                index = int(d_.seconds/3600) + int(d_.days * 24) + 1

                # Send Socket Updates
                if index < len(loaded_data):
                    new_content = loaded_data[index:]
                    self.last_point = new_content[-1]
                    for package in new_content:
                        self.write_message(message=package)

            # Recurse
            threading.Timer(self._poll_timer, self.poll_data).start()
        except:
            pass

    def open(self):
        print("~ socket opened ~")
        loaded_data = self.load_data()
        self.last_point = loaded_data[-1]
        for package in loaded_data:
            self.write_message(message=package)
        if self.thread == 0:
            self.thread = threading.Timer(self._poll_timer, self.poll_data)
            self.thread.start()

    def on_close(self):
        print("~ socket closed ~")
        self.thread.cancel()
        self.thread = 0
        self.slept = False
        self.last_point = ['null', '']

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
