# Run ping command

URL=www.google.ca
PING_LIMIT=40

echo "Checking ping, will run traceroute if ping is over ${PING_LIMIT}"

while true; do
  V=$(ping $URL -c1 | awk '{print substr($7,6)}')
  if [[ ${V%.*} -gt PING_LIMIT ]]; then
    echo 'greater'
    traceroute $URL
  fi
  sleep 1
done

# If the ping is above the limit, let's run the following command:

#traceroute $URL

