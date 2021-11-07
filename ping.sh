# Pull in environment variables - we use $CODE_PATH here
set -o allexport
source .env
set +o allexport

# If process ID exists for previous invocations of this command, check for it and kill it.
PID_FILE=/tmp/pinger.pid
if [ -f "$PID_FILE" ]; then
  PID=`cat $PID_FILE`
  pkill $PID
  echo "attempting to kill process $PID"
fi

# If we have CODE_PATH set in our environment, use this as the path to the repo's executable
if [ -d "$CODE_PATH" ]; then
  nohup $CODE_PATH/pinger/ping.py &
else
  # Otherwise, assume it's in the flat directory '~/code'
  nohup ~/code/pinger/ping.py &
fi

# Add PID to the file to log that the process is running.
PID=$!
echo "creating process $PID"
echo $PID > $PID_FILE
