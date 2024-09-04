#!/usr/bin/env bash

PROJECT_PATH=$(pwd)

docker run -d \
  --name pattern-recognition-test-traffic-client \
  --volume "${PROJECT_PATH}"/docker/tests/traffic-client/app:/app \
  --network tests_kafka-net \
  jstefl/pattern-recognition-test-traffic-client-image:latest