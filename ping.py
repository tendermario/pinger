#!/Users/marioviens/coding/projects/pinger/.venv/bin/python

import time
import subprocess
import platform
import re
import sys
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv('URL')
LOG_GROUP_NAME = os.getenv('LOG_GROUP_NAME')
LOG_STREAM_NAME = os.getenv('LOG_STREAM_NAME')
# PRINT_PING will print ms to output if True
# In the .env file, make this be any string to be True. If left blank, it will be False.
PRINT_PING = bool(os.getenv('PRINT_PING'))

operating_sys = platform.system()
logsClient = boto3.client('logs')

def ping(ip):
    ping_command = ['ping', ip, '-c 1']
    ping_output = subprocess.run(ping_command,shell=False,stdout=subprocess.PIPE)
    message = str(ping_output.stdout)
    index = message.find('time=')
    endIndex = message.find(' ms')
    time = message[index+5:endIndex]
    return time

def getSequenceToken():
    response = logsClient.describe_log_streams(
        logGroupName=LOG_GROUP_NAME,
        logStreamNamePrefix=LOG_STREAM_NAME
    )
    return response['logStreams'][0]['uploadSequenceToken']


# Get the sequence token to upload to CloudWatch
sequenceToken = getSequenceToken()

print("Checking ping every second and sending it to CloudWatch")

if (PRINT_PING):
        print("Printing ping (in ms)")

while(True):
    # Get ping in ms
    ping_time = ping(URL)
    timestamp = int(round(time.time() * 1000))
    if (PRINT_PING):
        print(ping_time)

    # Send data to cloudwatch
    try:
        response = logsClient.put_log_events(
            logGroupName=LOG_GROUP_NAME,
            logStreamName=LOG_STREAM_NAME,
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
        print("Warning: could not post to CloudWatch. Will naively try with a new token...")
        message = e.response['Error']['Message']
        index = message.find('is:')
        sequenceToken = message[index+4:]


    time.sleep(1)



