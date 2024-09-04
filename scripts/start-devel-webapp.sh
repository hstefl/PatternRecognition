#!/usr/bin/env bash

PROJECT_PATH=$(pwd)

docker run \
  -it \
  --publish 5151:5000 \
  --volume sqlite_data:/data \
  --network tests_kafka-net \
  --env-file "${PROJECT_PATH}/.env" \
  --name pattern-recognition-webapp \
  jstefl/pattern-recognition-webapp:latest