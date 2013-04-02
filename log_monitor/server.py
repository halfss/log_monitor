#!/usr/bin/env python2.7
#coding=utf8

import os
import sys
import socket
import threading
import SocketServer
import re

from conf import *
from lib import sendEmail,daemonize


HOST = dict(monitor_conf.items('DEFAULT'))['server']
PORT = int(dict(monitor_conf.items('DEFAULT'))['port'])
ALARM = dict(monitor_conf.items('SERVER'))['alarm'].split(',')

p_dir='/var/log/log_monitor'
if not os.path.exists(p_dir):
    os.mkdir(p_dir)

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(40960)
        print self.client_address[0],data
        data = eval(data)
        cur_thread = threading.current_thread()
        if re.findall(r'ERROR',data['content']) or re.findall(r'error',data['content']):
            if sendEmail(ALARM,"%s/%s" % (data['hostname'],self.client_address[0]),'<font color=red>'+data['content']+'</font>'):
              print "发送邮件成功！"
            else:
              print "发送邮件失败！"

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def start():
    daemonize(stdout=p_dir+'/log_monitorout.log', stderr=p_dir+'/log_monitorerr.log',pidfile=p_dir+'/log_monitorpid.txt')
    global HOST, PORT

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    server.serve_forever()

if __name__=="__main__":
    start()
