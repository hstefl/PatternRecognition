#!/usr/bin/env bash

docker build --no-cache -t jstefl/pattern-recognition-recognizer:latest -f docker/recognizer/Dockerfile .
