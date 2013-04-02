#!/usr/bin/env python

import os,sys
import time
import socket

from lib import daemonize
from conf import *


HOST = dict(monitor_conf.items('DEFAULT'))['server']
PORT = int(dict(monitor_conf.items('DEFAULT'))['port'])


listen_file = dict(monitor_conf.items('CLIENT'))['monitor_file'].split(',')
interval = int(dict(monitor_conf.items('CLIENT'))['interval'])

p_dir=sys.path[0]
def data_send(line):
  try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    s.send(line)
  except Exception,e:
    print e
  finally:
    s.close()

def tail_f(filess):
    hostname = socket.gethostname()
    interval=1.0
    i=1
    try:
        files=file(filess,'r')
    except IOError:
        print 'fils is not exists,pass'
        return 'file is not exists'
    while True:
        where=files.tell()
        lines=files.readlines()
        if not lines:
            time.sleep(interval)
            i+=1
            if i>300:
                files=file(filess,'r')
                files.seek(0)
            else:
                files.seek(where)
        else:
            i=1
            data = {}
            data['hostname'] = hostname
            data['filename'] = filess
            data['content'] = str(lines)
            data_send(str(data))
def monitor():
    for files in listen_file:
        tail_f(files)

def daemonize(stdout='/dev/null', stderr=None, stdin='/dev/null',pidfile=None ):
        '''
        This forks the current process into a daemon.
        The stdin, stdout, and stderr arguments are file names that
        will be opened and be used to replace the standard file descriptors
        in sys.stdin, sys.stdout, and sys.stderr.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
        may not appear in the order that you expect.
        '''
        # Do first fork.
        try:
                pid = os.fork()
                if pid > 0: sys.exit(0) # Exit first parent.
        except OSError, e:
                sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
                sys.exit(1)
        # Decouple from parent environment.
        os.chdir("/")
        os.umask(0)
        os.setsid()

        # Do second fork.
        try:
                pid = os.fork()
                if pid > 0: sys.exit(0) # Exit second parent.
        except OSError, e:
                print 'second fork error'
                sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
                sys.exit(1)
        # Open file descriptors and print start messag
        if not stderr: stderr = stdout
        si = file(stdin, 'r')
        so = file(stdout, 'w')
        se = file(stderr, 'a+', 0)
        pid = str(os.getpid())
        print "Start with Pid: %s\n"  % pid
        sys.stderr.flush()
        if pidfile: file(pidfile,'w').write("%s\n" % pid)
        # Redirect standard file descriptoris.
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

def start():
    daemonize(stdout=p_dir+'/log_monitorout_clientout.log', stderr=p_dir+'/log_monitor_client_err.log',pidfile=p_dir+'/log_monitor_clientpid.txt')
    monitor()


if __name__=="__main__":
    monitor()
