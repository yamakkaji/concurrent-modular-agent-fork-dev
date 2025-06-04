from . import start, stop
import time
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            start()
        elif sys.argv[1] == "stop":
            stop()
        elif sys.argv[1] == "restart":
            stop()
            start()
        else:
            print("Invalid argument. Use 'start' or 'stop'.")
    else:
        print("No argument provided. Use 'start' or 'stop'.")

