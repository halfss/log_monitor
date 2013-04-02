#coding=utf8

import os
import ConfigParser


monitor_conf_file = '/etc/log_monitor/log_monitor.conf'
monitor_conf=ConfigParser.RawConfigParser()

if os.path.exists(monitor_conf_file):
    monitor_conf.read(monitor_conf_file)
else:
    monitor_conf.read(os.path.abspath('.')+'/log_monitor.conf')


if __name__ == '__main__':
    print dir(monitor_conf)
    print dict(monitor_conf.items('DEFAULT'))['server']
    print monitor_conf.items('CLIENT')
