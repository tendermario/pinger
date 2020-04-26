# Run ping command

URL=www.google.ca
PING_LIMIT=40

#echo "Checking ping, every second"

while true; do
  V=$(ping $URL -c1 | awk '{print substr($7,6)}')
  echo $V > testdata
  sleep 1
done

