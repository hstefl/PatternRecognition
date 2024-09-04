#!/usr/bin/env bash

# Starts traffic server and agent
docker run \
  --interactive \
  --tty \
  --rm \
  --publish 5111:5000 \
  --network tests_kafka-net \
  --name pattern-recognition-test-traffic-server \
  jstefl/pattern-recognition-test-traffic-server:latest
