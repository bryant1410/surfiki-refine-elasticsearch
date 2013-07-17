#!/bin/bash
PYTHONPATH=$PYTHONPATH:/root
PYTHONPATH=$PYTHONPATH:/root/refine
PYTHONPATH=$PYTHONPATH:/root/refine/jobs/refine
export PYTHONPATH
python /root/refine/startup.py
python /root/refine/tools/mapper_watcher.py &
