#!/bin/bash

if [ -f ".pid" ];then
  pkill -9 -P `cat .pid`
  kill -9 `cat .pid` > /dev/null 2>&1
  echo "kill gitlabtools server success"
else
  echo "gitlabtools server is not running! not need kill"
fi
