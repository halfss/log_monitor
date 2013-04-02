#coding=utf8


from setuptools import setup,find_packages

setup(
        name = 'log_monitor',
        version = '0.1',

        scripts=[
            'bin/log_monitor_server',
            'bin/log_monitor_client',
            ],
        packages=[
            'log_monitor'
            ],
        data_files=[
            ('/etc/log_monitor',['etc/log_monitor.conf']),
            ]
        )
