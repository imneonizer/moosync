import time
import sys
import os
import json
import datetime

class MoosyncDaemon:
    def __init__(self, config_path=None, interval=1):
        self.idx = 0
        self.interval = interval
        config_path = config_path or os.path.join(os.path.expanduser('~'), '.moosync.json')
        with open(config_path, "r") as f:
            self.config = json.loads(f.read())
    
    def log(self, msg="", limit=100):
        mode = "a"
        if self.idx % limit == 0:
            self.idx, mode = 0, "w"
        with open("/tmp/moosync_daemon.log", mode) as f:
            f.write(f"[{datetime.datetime.now()}]:{self.config.get('host')}-{self.config.get('serial')}, {msg}\n")
        self.idx += 1
    
    def start(self):
        while True:
            self.log("syncing")
            time.sleep(self.interval)

if __name__ == "__main__":
    MoosyncDaemon().start()