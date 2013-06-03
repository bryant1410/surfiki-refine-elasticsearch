#!/bin/bash
python /surfiki-refine-elasticsearch/startup.py
python /surfiki-refine-elasticsearch/tools/mapper_watcher.py &
