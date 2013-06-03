#!/bin/bash
pkill python
redis-cli -p 7778 -a surfikiMR  KEYS "*" | xargs redis-cli -p 7778 -a surfikiMR DEL
for file in `ls /surfiki-refine-elasticsearch/jobs/refine`
do
  if [[ "$file" != template ]]; then
    echo $file
    redis-cli -p 7778 -a surfikiMR sadd "surfiki::job-types" $file
    redis-cli -p 7778 -a surfikiMR set "surfiki::job-types::status::${file}" "INACTIVE" 
  fi
done
