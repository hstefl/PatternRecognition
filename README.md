Pattern Recognition
===================
This project captures network traffic, performs analysis, and provides simple reporting.

Implemented analysis: Open password detection

This project is just a "sandbox" for getting started with some technologies I found interesting.
It will always be considered a proof of concept and will never be meant for real-world usage.

The idea is to write a "system test" which demonstrates given ideas (like open password detection).

Technologies used: 
 * Python, Pytest, Testcontainers, Scapy, Flask, SQLAlchemy, Kafka-python-ng, Pandas
 * venv
 * Docker, Docker Compose
 * Kafka
 * Bash

NOTE: Almost everything is containerized, with the key use case being to create tests as mentioned above.
There is no focus on any different deployment than that.


Architecture
============
The idea is to have a agent collecting data (like network traffic) at an endpoint and send it 
into Kafka. From Kafka, it is taken by recognizers that perform specific analysis (like open password detection).
As soon as the recognizer finds a pattern/problem, it stores it to the database.
The web application reads and displays all reported recognitions.

Service
-------
Anything that can be identified, started, and stopped. The abstract class for services is in `core.Service`.

Agent
-----
Its purpose is to start other services that collect data at the endpoint. The agent is implemented in the class `core.Agent.Agent`.
Services for data collection are stored in the package `core.agent`. 

Recognizer
---------
Starts other services, which analyze data collected by agents. The recognizer is implemented in the class `core.Recognizer.Recognizer`.
Services for analyzing data are stored in the package `core.recognizer`.

Project structure
=========
 * `app/`: All project source code written in Python.
 * `app/core/`: Key modules of the project (like services, agents, recognizers).
 * `app/data/`: Modules for data manipulation from the database.
 * `app/webapp/`: Web application for showing information about found recognitions.
 * `docker/`: All Docker-related files (Dockerfiles, Docker Compose).
 * `docker/recognizer/`: Contains Dockerfile for describing the image for container starting services, spawning default recognizers.
 * `docker/tests/`: Contains images for generating/receiving traffic that can be captured. Contains key testing compose file.
 * `docker/webapp/`: Application showing any recognition.
 * `scripts/`: Bash scripts for development purposes (like building images and starting containers).
 * `tests/`: Tests for demonstrating the concept.
 * `requirements.txt`: All dependencies of the project, for development purposes.
 * `.env`: Definition of environment variables for containers.

Usage
=====
This is about testing the proof of concept, so the tests are the goal to execute.

Prerequisites
-------------
1. Docker and Docker Compose installed
2. Python
3. Bash (if you want to use scripts in `scripts/`, but they are for development only)

Versions used during development:
 * Docker 27.2.0
 * Docker Compose 1.29.2
 * Python 3.12.5
 * Fedora 40 (never tested anywhere else)

How
---
1. Clone the project: `git clone https://github.com/hstefl/PatternRecognition.git`
2. Navigate to the project root directory: `cd PatternRecognition`
3. Create the virtual environment: `python -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate` 
5. Download dependencies: `pip install -r requirements.txt`
6. Execute the test: `pytest tests/test_open_password_recognized.py`

Do not expect any output if everything goes well (expected scenario). This project is about studying the code.
The entry point for that can be the executed test.
