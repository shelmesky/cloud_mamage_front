#!/usr/bin/python
import pika
import sys
import time
import threading
from threading import Lock
import uuid
import simplejson
import Queue

import tornado.ioloop
import tornado.web


rabbitmq_server = "127.0.0.1"
username = "guest"
password = "guest"
virtual_host = "/"
frame_max_size = 131072

lock = Lock()

def gen_message_id():
    return uuid.uuid4().get_hex()


def sync(lock):
    def wrap(func):
        def wrapper(*args, **kwargs):
            lock.acquire()
            try:
                ret = func(*args, **kwargs)
            finally:
                lock.release()
            return ret
        wrapper.func_name = func.func_name
        wrapper.__doc__ = func.__doc__
        return wrapper
    return wrap


class Singleton(object):
    _instance = None
    _lock = lock or threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        """
        Singleton model
        """
        Singleton._lock.acquire()
        if not cls._instance:
            cls._instance = super(Admin_Receiver,cls).__new__(cls, *args, **kwargs)
        Singleton._lock.release()
        return cls._instance


class Admin_Receiver(threading.Thread):
    
    _instance = None
    _lock = lock or threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        """
        Singleton model
        """
        Singleton._lock.acquire()
        if not cls._instance:
            cls._instance = super(Admin_Receiver,cls).__new__(
                cls, *args, **kwargs)
        Singleton._lock.release()
        return cls._instance
    
    def __init__(self):
        super(Admin_Receiver,self).__init__()
        self.daemon = False
        self.node_list = {}
        self.result_list = []
        self.connect()
    
    def connect(self):
        """
        connect to rabbitmq server and declare exchange and queue.
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(virtual_host=virtual_host,
                        credentials=pika.PlainCredentials(username,password),frame_max=frame_max_size,
                        host=rabbitmq_server))
        self.connection1 = pika.BlockingConnection(pika.ConnectionParameters(virtual_host=virtual_host,
                        credentials=pika.PlainCredentials(username,password),frame_max=frame_max_size,
                        host=rabbitmq_server))

        self.channel1 = self.connection1.channel()
        self.channel1.exchange_declare(exchange='fanout',
                                 type='fanout',durable=True)

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='direct',type='direct',durable=True)
        self.channel.queue_declare(queue='direct_queue', durable=True)
        self.channel.queue_bind(exchange='direct',
                   queue='direct_queue',
                   routing_key='lb')
        
    def run(self):
        self.channel.basic_consume(self.callback,
                      queue='direct_queue',)
        self.channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        """
        callback function for direct exchange for receive return message from remote agent.
        """
        body = simplejson.loads(body)
        message_type = body['message_type']
        
        if message_type == "heartbeat":
            self.cache_node_list(body)
            
        if message_type == "work_report":
            self.result_list.append(body)
            
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    def send(self, message):
        """
        send message to a fanout exchange.
        """
        self.channel1.basic_publish(exchange='fanout',
                              routing_key='',
                              body=message)
        print "[x] Sent %r" % (message,)
    
    def cache_node_list(self, body):
        """
        cache a node list and update them immediately.
        """
        node_id = body['node_id']
        ctime = body['time']
        if node_id not in self.node_list:
            self.node_list[node_id] = ctime
            print "node %s online now..." % node_id
        for k,v in self.node_list.items():
            if int(time.time() - float(v)) >=3:
                self.node_list.pop(k)
                print "node %s offline..." % k
            else:
                self.node_list[node_id] = ctime
        
    @property
    def get_node_list(self):
        return [node_id for node_id,ctime in self.node_list.items()]
            
    def get_return(self, msg_id, timeout=3):
        """
        used to get return message from a direct exchange use a message id and run with a timeout parameter.
        """
        i = 0
        max_wait = timeout * 1000
        while 1:
            if i > max_wait:
                return "get_return_timeout"
            if self.result_list:
                for message in self.result_list:
                    if message['message_id'] == msg_id:
                        ret = message
                        return ret
            i += 1
            time.sleep(0.001)


Admin_Receiver_Thread = Admin_Receiver()
if not Admin_Receiver_Thread.is_alive():
    Admin_Receiver_Thread.start()


