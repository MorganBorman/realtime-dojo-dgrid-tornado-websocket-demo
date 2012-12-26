#!/usr/local/bin/python

import os
import sys
import socket

system_directory = os.path.dirname(os.path.abspath(__file__))

import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop

from WebSocketHandler import WebSocketHandler
from MainRequestHandler import MainRequestHandler

import UserStore

handlers = [
    (r'/', MainRequestHandler),
    (r'/ws', WebSocketHandler),
]

if __name__ == "__main__":
    tornado_app = tornado.web.Application(handlers,
                                          debug=True,
                                          template_path=system_directory+"/templates", 
                                          static_path=system_directory+"/static")
    
    tornado.options.parse_command_line()
    
    tornado_http = tornado.httpserver.HTTPServer(tornado_app)
    tornado_http.bind(8080, family=socket.AF_INET)
    tornado_http.start()
    
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print "\nReceived KeyboardInterrupt exiting..."
