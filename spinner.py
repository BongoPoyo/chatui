import sys
import time
import threading
import itertools


class Spinner:
    def __init__(self, message="Loading"):
        self.message = message
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._spin, daemon=True).start()

    def _spin(self):
        spinner = itertools.cycle(["|", "/", "-", "\\"])
        while self.running:
            sys.stdout.write(f"\r{self.message} {next(spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)

    def stop(self):
        self.running = False
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()
