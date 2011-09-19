#!/usr/bin/python

from subprocess import *

p = Popen(["cat", "/var/spool/syslog-notify"], stdout=PIPE)

for line in p.stdout:
    #print(line.decode())
    arg = ["gdbus","call"]
    arg.append("--session")
    arg.append("--dest")
    arg.append("org.freedesktop.Notifications")
    arg.append("--object-path")
    arg.append("/org/freedesktop/Notifications")
    arg.append("--method")
    arg.append("org.freedesktop.Notifications.Notify")
    arg.append("my_app_name")
    arg.append("42")
    arg.append("gtk-dialog-info")
    arg.append("syslog-ng")
    arg.append(line.decode()) 
    arg.append("[]")
    arg.append("{}") 
    arg.append("5000")
    call(arg)
