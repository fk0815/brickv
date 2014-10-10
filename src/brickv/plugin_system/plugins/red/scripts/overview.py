#!/usr/bin/env python2 

import psutil
import sys

with open("/proc/uptime", "r") as utf:
    print utf.readline().split(".")[0]

du = psutil.disk_usage("/")
if len(sys.argv) < 2:
    print psutil.cpu_percent(2)
else:
    print psutil.cpu_percent(float(sys.argv[1]))
print psutil.used_phymem()
print psutil.TOTAL_PHYMEM
print du.used
print du.total