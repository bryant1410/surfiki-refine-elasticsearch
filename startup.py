#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from os.path import abspath, dirname, join
import httplib
import time
import json
import os, subprocess
from subprocess import call
def job_port(type):
    f = open("port.config")
    res = '9999'
    for line in f.readlines():
        line = line.strip('\n')
        key = line.split("=")[0]
        val = line.split("=")[1]
        if (key == type):
          res = val
    f.close()
    return res

def run_job(jobtype):
    for r,d,f in os.walk("/root/refine/jobs/refine/"+jobtype):
        for files in f:
            if files.endswith("_mapper.py"):
                filename = files
                for line in open(os.path.join(r,files)):
                    if line.startswith("class"):
                        classtwo = line.split(' ')[1].split('(')[0]
    classone = filename[:-3]
    mapperclass = classone+"."+classtwo
    # Start the App in backgorund process
    os.popen('python refine/app/server.py --redis-port=6379 -p '+ job_port(jobtype) + ' --redis-pass=surfikiMR --config-file=jobs/refine/' + jobtype + '/app_config.py &')
    os.popen('python refine/worker/mapper.py --mapper-key=map-key-'+jobtype+'1 --mapper-class='+jobtype+'.'+mapperclass+' --redis-port=6379 --redis-pass=surfikiMR &')

os.popen('python refine/web/server.py --redis-port=6379 --redis-pass=surfikiMR --config-file=./refine/web/config.py &')
f = open("/var/spool/cron/crontabs/root")
for line in f.readlines():
    line = str(line.strip('\n'))
    if "XGET" in line:
        lines = line.split("/")
        last = lines[len(lines) - 1]
        jobtype = last[0:last.index('.')]
        run_job(jobtype)
f.close()
