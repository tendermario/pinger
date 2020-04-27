# Run ping command

URL=www.google.ca
PING_LIMIT=50
SECONDS=3600

echo "Checking ping for ${SECONDS} seconds, will total up the amount of times ping was high"

time=0
over50=0
over100=0
over200=0
while [ 3600 -gt $time ]; do
  V=$(ping $URL -c1 | awk '{print substr($7,6)}')
  ping=${V%.*}
  if [[ ${V%.*} -gt 50 ]]; then
    echo "Over 50"
    over50=$(( $over50 + 1 ))
    echo "ping: $ping"
  fi
  if [[ ${V%.*} -gt 100 ]]; then
    echo "Over 100"
    over100=$(( $over100 + 1 ))
  fi
  if [[ ${V%.*} -gt 200 ]]; then
    echo "Over 200"
    over200=$(( $over200 + 1 ))
  fi
  sleep 1
  time=$(( $time + 1 ))
done

echo "Spent an hour, over 50ms ping happened for $over50 s. over 100ms: $over100 s, over 200ms: $over200 s."

