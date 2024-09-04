#!/usr/bin/env python3

#
# Usage:
# This scripts start agent in foreground. It can be stopped with ctrl-C or so.
#

import sys
import os
import atexit

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/app")

from core.Recognizer import Recognizer
import data.init_db


def main():
    # Make sure that DB is initialized
    data.init_db.main()

    recognizer = Recognizer()

    def shutdown_hook():
        nonlocal recognizer
        recognizer.stop()

    atexit.register(shutdown_hook)

    recognizer.start()


if __name__ == "__main__":
    main()
