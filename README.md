# Pinger

A tool to test what route is slow.

## For a simple output in ms

Just run:

```
./shell-ping/pinger.sh
```

## To send data to CloudWatch and automatically monitor your system

_(Note this is only tested with a Mac system for now...)_

- Create an AWS account, or log in to one.
- Create a virtualenv with python3 and load it.
- Install awscli and boto3: `pip install -r requirements.txt`
- Configure your aws cli so you are authenticated to publish to your account: `aws configure` Reference: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
- Create a log group, and a log stream here: https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#logsV2:log-groups
  - TODO: make this automated with the aws cli and aws-cdk or cloudformation template
- Make sure those names are used in the ping.py script
- Run `./ping.py` to make sure it works and there are no errors.
- Check the log stream to make sure it is populating correctly
- In CloudWatch > Log groups > select your log group.
- Click "Metric filters" and add a filter with the Filter Pattern `[time]` and Next > Metric value is set to `$time`
- In CloudWatch > Dashboards, create a dashboard, and create a line graph based on this metric.

## To enable it at startup

(Still in progress, the plist file doesn't seem to invoke, PLEASE HELP)

- Run your virtualenv python in the hashbang:
-   Run `which python` while in your virtualenv
-   Update the first line in `ping.py` to it so it looks like something like:

```
#!/Users/marioviens/coding/projects/pinger/.venv/bin/python
```

- Copy the .plist file to your launch daemons folder and replace <path> with the path to your pinger.py executable. On a Mac the loanch daemon folder is: `/Library/LaunchDaemons/`
- Add the file to the launchctl registry `launchctl load -w /Library/LaunchDaemons/pinger.plist`
- (Still trying to figure out) enable this and confirm it runs successfully on system start... `sudo launchctl enable system/com.pinger.tendermario`

## To run on terminal window launch

This is a workaround to the above for now: when you open terminal, it runs this shell script and puts
it in the background. You can close the terminal and theoretically the process should be running in the background. (TEST THIS PLS)

- Add running the `ping.sh` in your dot


## TO INVESTIGATE

how to translate this into data:

`2021-11-05T22:38:20.695-07:00	NG www.google.ca (142.250.217.99): 56 data bytes\n\n--- www.google.ca ping statistics ---\n1 packets transmitted, 0 packets received, 100.0% packet loss\n`

I think it 

## Example

![Example](docs/example.png "Example Dashboard")

MIT License.
