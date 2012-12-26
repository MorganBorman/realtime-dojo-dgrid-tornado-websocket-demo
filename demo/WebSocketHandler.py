import tornado.websocket
import tornado.web

import json
import os
import shutil

from ws_exceptions import InsufficientPermissions, InvalidStateError, MalformedMessage

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    message_handlers = {}
    
    streams = [] # holds a list of all the stream names
    subscribers = {} # key: stream name, value: list of websocket connections
    
    subscriptions = [] # holds a list of subscribed stream names
        
    @staticmethod
    def register_stream(stream_name):
        if not stream_name in WebSocketHandler.streams:
            WebSocketHandler.streams.append(stream_name)
        
    @staticmethod
    def publish(stream_name, message_data):
        if stream_name in WebSocketHandler.subscribers.keys():
            for socket_connection in WebSocketHandler.subscribers[stream_name]:
                if socket_connection is not None:
                    try:
                        socket_connection.write_message(message_data)
                    except AttributeError:
                        pass
        
    def subscribe(self, stream_name):
        if not stream_name in WebSocketHandler.streams:
            raise InvalidStateError("Unknown stream.")
        
        self.subscriptions.append(stream_name)
        
        if not stream_name in WebSocketHandler.subscribers.keys():
            WebSocketHandler.subscribers[stream_name] = []
        
        WebSocketHandler.subscribers[stream_name].append(self)
        
    def unsubscribe(self, stream_name):
        if stream_name in self.subscriptions:
            self.subscriptions.remove(stream_name)
            
        if stream_name in WebSocketHandler.subscribers.keys():
            if self in WebSocketHandler.subscribers[stream_name]:
                WebSocketHandler.subscribers[stream_name].remove(self)
    
    def open(self):
        self.subscriptions = []

    def on_message(self, message):
        msg = json.loads(message)
        
        if not "type" in msg.keys():
            raise MalformedMessage()
        
        msgtype = msg["type"]
        
        if not msgtype in self.message_handlers.keys():
            raise MalformedMessage()
            
        self.message_handlers[msgtype](self, msg)

    def on_close(self):
        if len(self.subscriptions) > 0:
            for stream_name in self.subscriptions[:]:
                self.unsubscribe(stream_name)

class messageHandler(object):
    def __init__(self, message_type, required_fields=[]):
        self.message_type = message_type
        self.required_fields = required_fields

    def __call__(self, f):
        if type(f) == type:
            f = f(self.message_type, self.required_fields)
        
        def handler(socket_connection, message):
            for field in self.required_fields:
                if not field in message.keys():
                    raise MalformedMessage()
                
            f(socket_connection, message)
        
        self.handler = handler
        
        WebSocketHandler.message_handlers[self.message_type] = handler
        
        return f
        
class StreamHandle(object):
    def __init__(self, stream_name):
        self.stream_name = stream_name
        
        WebSocketHandler.register_stream(stream_name)
        
    def publish(self, message_data):
        WebSocketHandler.publish(self.stream_name, message_data)
        
@messageHandler("subscribe_request", ['stream'])
def handle_admin_module_tree_request(socket_connection, message):
    """
    Subscribes this websocket connection to a message stream.
    """
    socket_connection.subscribe(message['stream'])
    
    result_message = {'type': 'subscribe_ack',
                      'stream': message['stream']}
                      
    socket_connection.write_message(json.dumps(result_message))
