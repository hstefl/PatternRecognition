#!/usr/bin/env bash

docker build --no-cache -t jstefl/pattern-recognition-test-traffic-client:latest -f docker/tests/traffic-client/Dockerfile .