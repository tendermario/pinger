#!/Users/marioviens/coding/projects/pinger/.venv/bin/python

import time
import subprocess
import platform
import re
import sys

import boto3

PRINT_PING = True # Update me to True to print the ms to output

URL = 'www.google.ca'
operating_sys = platform.system()
logsClient = boto3.client('logs')
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

def getSequenceToken():
    response = logsClient.describe_log_streams(
        logGroupName=logGroupName,
        logStreamNamePrefix=logStreamName
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
        print("Warning: could not post to CloudWatch. Will naively try with a new token...")
        message = e.response['Error']['Message']
        index = message.find('is:')
        sequenceToken = message[index+4:]


    time.sleep(1)



