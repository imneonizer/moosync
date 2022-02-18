import time
import sys
import os
import json
import datetime

if __name__ == "__main__":
    if len(sys.argv) == 1: exit(1)

    # cuda visibile devices
    gpus = sys.argv[1]
    
    # read token from config file
    with open(os.path.join(os.path.expanduser('~'), '.moosync.json'), "r") as f:
        config = json.loads(f.read())
    
    # event loop
    idx = 0
    while True:
        # empty log file at every 100th iterations
        mode = "w" if idx % 100 == 0 else "a"
        with open("/tmp/moosync_daemon.log", mode) as f:
            f.write(
                f"[{datetime.datetime.now()}]: SERIAL={config.get('serial')}, HOST={config.get('host')}, CUDA_VISIBLE_DEVICES={gpus}\n"
            )
        
        time.sleep(1)
        idx += 1