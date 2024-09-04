"""
Test suite for the Pattern Recognition system.

This project is POC and the goal is to get me familiar with listed topic not to create project for real world usage.
 - Python (pytest, testcontainers, scapy, flask, SQLAlchemy)
 - Containers (docker, docker compose)
 - Kafka (writing and reading messages)
 - Panda (simple dataframe)
 - Packet sniffing/analyzing
 - Effective development (implementation nad debugging) of containerized project.

This file contains one system test - verification that system is able to detect open password in the network traffic.

NOTE: First run takes minutes each subsequent seconds (in case that images are not removed).
Installed images:
    jstefl/pattern-recognition-test-traffic-server   latest    526MB
    jstefl/pattern-recognition-webapp                latest    379MB
    jstefl/pattern-recognition-recognizer            latest    193MB
    jstefl/pattern-recognition-test-traffic-client   latest    109MB
    obsidiandynamics/kafdrop                         latest    623MB
    confluentinc/cp-kafka                            7.0.1     780MB
    confluentinc/cp-zookeeper                        7.0.1     780MB


The architecture of system is described in the README.md file.
"""

import os
import re
import subprocess
import time

import pytest
import requests
import logging
from testcontainers.compose import DockerCompose


@pytest.fixture(scope="module")
def docker_compose():
    """
     Prepare a testing environment defined in docker compose `PROJ_ROOT/docker/tests/testing-environment.yml`.

     Started services:
     - Recognizer:
       Recognize suspicious patterns and reports them.
     - Webapp:
       Displays recognized suspicious patterns.
     - Traffic server with agent:
       Testing component, mock web application providing login interface.
       There is also started agent, that listen network traffic and store it into Kafka for further analysis.
     - Traffic client:
       Testing services authenticate to mock web application provided by traffic server service.
    """

    project_root = get_project_directory()
    test_compose_dir = project_root + "/docker/tests"
    os.environ['BUILD_CONTEXT'] = project_root

    with DockerCompose(project_root, compose_file_name="docker/tests/testing-environment.yml", build=True) as compose:
        try:
            # Wait for services to be started
            wait_for_logs(compose, "recognizer", "Connection complete")
            wait_for_logs(compose, "webapp", "Running on")
            wait_for_logs(compose, "traffic-server-with-agent", "INFO spawned: 'flask' with pid")
            wait_for_logs(compose, "traffic-server-with-agent", "INFO spawned: 'agent' with pid")
            wait_for_logs(compose, "traffic-client", "traffic client started")
        except Exception as e:
            logging.error("Error starting Docker services: %s", e)
            subprocess.run(
                ["docker-compose", "-f", project_root + f"/docker/tests/testing-environment.yml", "logs"],
                check=False)
            raise

        yield compose  # Provide the compose object for use in the tests


def test_web_service(docker_compose):
    """
    Testing that login request send via HTTP is detected as "open password in network traffic".

    Preconditions:
     - Started services: traffic client and server with agent, recognizer, webapp
    Test:
     - Send POST request over HTTP from traffic client to traffic server.
    Expected outcome:
     - Message in webapp that open password was detected in network.
    """

    webapp_address, webapp_port = docker_compose.get_service_host_and_port("webapp")
    traffic_server_port = docker_compose.get_container("traffic-server-with-agent").get_publisher().TargetPort
    traffic_server_address = docker_compose.get_container("traffic-server-with-agent").Name

    # Send the POST requests over HTTP
    docker_compose.exec_in_container(
        [
            "curl",
            "-X",
            "POST",
            "-d",
            "username=testuser&password=testpassword",
            "http://" + traffic_server_address + ":" + str(traffic_server_port) + "/login"],
        "traffic-client")

    # Let the system process the event
    time.sleep(5)

    # Retrieve webapp message list.
    response = requests.get("http://" + webapp_address.replace("0.0.0.0", "localhost") + ":" + str(webapp_port))

    # Check whether page is found and contains warning about open password in a network.
    assert response.status_code == 200
    assert "Open password detected in network" in response.text


def wait_for_logs(compose, service_name, log_message, timeout=20, max_retries=5):
    """
    Wait until the service has `log_message` in a log. Wait for a timeout at most.
    """
    retries = 0
    while retries < max_retries:
        start_time = time.time()
        while time.time() - start_time < timeout:
            logs = compose.get_logs(service_name)
            for log in logs:
                if re.search(log_message, log):
                    return True
            time.sleep(1)
        retries += 1
        timeout *= 2  # Exponential backoff
    raise TimeoutError(f"Service {service_name} did not output the expected log message within {timeout} seconds after {max_retries} retries")


def get_project_directory():
    """
    Returns project root directory.
    """
    # Get the absolute path of the current file
    current_file_path = os.path.abspath(__file__)

    # Get the directory one level above
    parent_directory = os.path.dirname(os.path.dirname(current_file_path))

    return parent_directory
