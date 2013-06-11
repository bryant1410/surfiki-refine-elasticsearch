#!/bin/bash
function getPropertyFromFile()
{
  propertyName=`echo $1 | sed -e 's/\./\\\./g'`
  fileName=$2;
  cat $fileName | sed -n -e "s/^[ ]*//g;/^#/d;s/^$propertyName=//p" | tail -1
}

pkill python
port=`getPropertyFromFile REDIS_PORT ./refine/web/config.py`
redis-cli -p $port -a surfikiMR  KEYS "*" | xargs redis-cli -p $port -a surfikiMR DEL
for file in `ls /root/refine/jobs/refine`
do
  if [[ "$file" != template ]]; then
    echo $file
    redis-cli -p $port -a surfikiMR sadd "surfiki::job-types" $file
    redis-cli -p $port -a surfikiMR set "surfiki::job-types::status::${file}" "INACTIVE" 
  fi
done
