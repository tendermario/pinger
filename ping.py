#!/usr/bin/env python3

import time
import subprocess
import platform
import re

import boto3


URL = 'www.google.ca'
operating_sys = platform.system()
logs = boto3.client('logs')
logGroupName = 'shaw_ping'
logStreamName = 'personal_macbook'


def ping(ip):
    ping_command = ['ping', ip, '-c 1']
    ping_output = subprocess.run(ping_command,shell=False,stdout=subprocess.PIPE)
    message = str(ping_output.stdout)
    index = message.find('time=')
    endIndex = message.find(' ms')
    time = message[index+5:endIndex]
    return time

sequenceToken = '1'

print("Checking ping every second and sending it to cloudwatch")
while(True):
    # Get ping in ms
    ping_time = ping(URL)
    timestamp = int(round(time.time() * 1000))
    # COMMENT IN FOR PING
    #print(ping_time)

    # Send data to cloudwatch
    try:
        response = logs.put_log_events(
            logGroupName='shaw_ping',
            logStreamName='personal_macbook',
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': ping_time
                },
            ],
            sequenceToken=sequenceToken
        )
        sequenceToken = response['nextSequenceToken']
    except Exception as e:
        print("Warning: could not post to CloudWatch")
        message = e.response['Error']['Message']
        index = message.find('is:')
        sequenceToken = message[index+4:]

    time.sleep(1)



