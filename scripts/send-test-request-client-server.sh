#!/usr/bin/env bash

# Prerequisites: traffic server started on and serving on port 5000 (default)

ADDRESS=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pattern-recognition-test-traffic-server)

docker run --rm -it \
  --name pattern-recognition-test-traffic-send-request \
  --network tests_kafka-net \
  jstefl/pattern-recognition-test-traffic-client:latest
  curl -X POST -d "username=testuser&password=testpassword" http://"${ADDRESS}":5000/login
