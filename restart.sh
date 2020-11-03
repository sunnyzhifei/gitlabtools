#!/bin/bash

pid=`ps -ef |grep 'python3 main.py'|grep -v 'grep'|awk '{print $2}'`

if [ ${pid} ]; then
  echo "kill gitlabtools server: ${pid}"
  kill -9 ${pid}
else
  echo 'gitlabtools server is not running! not need kill' 
fi


nohup python3 main.py >> job.log 2>&1 &
 
echo "gitlabtools server start sucess"
