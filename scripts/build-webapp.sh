#!/usr/bin/env bash

docker build --no-cache -t jstefl/pattern-recognition-webapp:latest -f docker/webapp/Dockerfile .
