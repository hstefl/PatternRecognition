#!/usr/bin/env python3

#
# Usage:
# This scripts start agent in foreground. It can be stopped with ctrl-C or so.
#

import atexit
import os
import sys

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/app")
from core.Agent import Agent


def main():
    gobbler = Agent()

    def shutdown_hook():
        nonlocal gobbler
        gobbler.stop()

    atexit.register(shutdown_hook)

    gobbler.start()


if __name__ == "__main__":
    main()
