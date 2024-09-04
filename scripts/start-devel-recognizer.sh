#!/usr/bin/env bash

PROJECT_PATH=$(pwd)

# Create Docker volume for saving SQLLite (testing DB) data
docker volume create sqlite_data

docker run -d \
  --rm \
  --name pattern-recognition-recognizer \
  --volume sqlite_data:/data \
  --network tests_kafka-net \
  --env-file "${PROJECT_PATH}/.env" \
  jstefl/pattern-recognition-recognizer:latest