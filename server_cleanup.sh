#!/bin/bash
pkill python
redis-cli -p 6379 -a surfikiMR  KEYS "*" | xargs redis-cli -p 6379 -a surfikiMR DEL
for file in `ls /root/refine/jobs/refine`
do
  if [[ "$file" != template ]]; then
    echo $file
    redis-cli -p 6379 -a surfikiMR sadd "surfiki::job-types" $file
    redis-cli -p 6379 -a surfikiMR set "surfiki::job-types::status::${file}" "INACTIVE" 
  fi
done
