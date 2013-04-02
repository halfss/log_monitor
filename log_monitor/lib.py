#!/usr/bin/env python2.7
#coding=utf8

import os
import sys

import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib

from conf import *


server = dict(monitor_conf.items('SERVER'))['server']
user = dict(monitor_conf.items('SERVER'))['user']
passwd = dict(monitor_conf.items('SERVER'))['passwd']
fromAdd = dict(monitor_conf.items('SERVER'))['fromadd']


def sendEmail(toAdd,subject,htmlText):
    strTo = ','.join(toAdd)
    # 设定root信息
    msgRoot = email.MIMEMultipart.MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = fromAdd
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgText = email.MIMEText.MIMEText(htmlText, 'html', 'utf-8')
    msgAlternative.attach(msgText)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(server)
        smtp.login(user, passwd)
        for i in toAdd:
            smtp.sendmail(fromAdd,i, msgRoot.as_string())
        smtp.quit()
        return True
    except Exception,e:
        print str(e)
        return False

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

if __name__ == '__main__' :
    sendEmail(['ljvsss@gmail.com'],'','<font color=red>red</font>')
