#!/bin/bash

# delete span
span=30

# get path of log dir
currentPath=`pwd`
logPath=${currentPath%scripts}log

# find del target
echo '-----------------------------------' >> rmtarget.log
date >> rmtarget.log
find $logPath -atime +$span -type f | grep -v "ipocc\.log$" | grep -v "\.conf" >> rmtarget.log

# count remove target
count=`find $logPath -atime +$span -type f | grep -v "ipocc\.log$" | grep -v "\.conf" | wc -l`

# exit when no target
if [ $count -eq 0 ]; then
  echo "no target" >> rmtarget.log
  exit 0
fi

# remove
find $logPath -atime +$span -type f | grep -v "ipocc\.log$" | grep -v "\.conf" | xargs rm

