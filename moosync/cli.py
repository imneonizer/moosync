import argparse
import getpass
import sys
from .moosync import moosync
import os
import json
import uuid

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--gpus", help="CUDA_VISIBLE_DEVICES", required=False, default="")
    ap.add_argument("-t", "--token", help="auth token", required=False, default="")
    ap.add_argument("-a", "--api", help="api address", required=False, default="http://localhost:5000")
    
    ap.add_argument("-l", "--logs", help="print moosync logs", action="store_true", required=False, default=False)
    ap.add_argument("-ls", "--list", help="list gpus info and running background syncs", action="store_true", required=False, default=False)
    ap.add_argument("-k", "--kill", help="stop running background syncs", action="store_true", required=False, default=False)
    
    args = ap.parse_args()
    return ap, args

def main():
    ap, args = parse_args()
    
    if args.token:
        serial = int(str(uuid.UUID(int=uuid.getnode()).node)[:-4])
        moosync.login(args.token, args.api, serial)
    
    elif args.logs:
        os.system("tail -F /tmp/moosync_daemon.log")
    
    elif args.list:
        moosync.list_background_syncs()
    
    elif args.kill:
        moosync.stop_background_sync(pprint=True)
    
    elif args.gpus:
        gpus = None
        try:
            gpus = moosync.start(args)
        except KeyboardInterrupt: pass
        if gpus:
            os.environ['CUDA_VISIBLE_DEVICES'] = gpus
            sys.stdout.write(str(gpus))
    
    else:
        ap.print_help()

if __name__ == "__main__":
    main()