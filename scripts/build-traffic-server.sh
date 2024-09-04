#!/usr/bin/env bash

docker build --no-cache -t jstefl/pattern-recognition-test-traffic-server:latest -f docker/tests/traffic-server/Dockerfile .
