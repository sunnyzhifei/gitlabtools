#!/bin/bash

nohup python3 main.pyc >> job.log 2>&1 & echo $! > .pid
 
echo "gitlabtools server start sucess!"
