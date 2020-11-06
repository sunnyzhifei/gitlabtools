#!/bin/bash

nohup python3 main.py >> job.log 2>&1 & echo $! > .pid
 
echo "gitlabtools server start sucess!"
