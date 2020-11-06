#!/bin/bash

if [ -f ".pid" ];then
	pkill -9 -P `cat .pid`
	echo "kill gitlabtools server success"
else
	echo "gitlabtools server is not running! not need kill"
fi
