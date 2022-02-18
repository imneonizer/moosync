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
    
    ap.add_argument("-u", "--username", help="login username", required=False, default="")
    ap.add_argument("-p", "--password", help="login password", required=False, default="")
    ap.add_argument("-a", "--api", help="api address", required=False, default="http://localhost:5000")
    
    ap.add_argument("-l", "--list", help="list running background syncs", action="store_true", required=False, default=False)
    ap.add_argument("-k", "--kill", help="stop running background syncs", action="store_true", required=False, default=False)
    
    args = ap.parse_args()
    return ap, args

def main():
    ap, args = parse_args()
    
    if args.username and args.password:
        serial = int(str(uuid.UUID(int=uuid.getnode()).node)[:-4])
        moosync.login(args.username, args.password, args.api, serial)
    
    elif args.list:
        moosync.list_background_syncs()
    
    elif args.kill:
        moosync.stop_background_sync(pprint=True)
    
    elif args.gpus:
        gpus = moosync.start(args)
        if gpus:
            os.environ['CUDA_VISIBLE_DEVICES'] = gpus
            sys.stdout.write(str(gpus))
    
    else:
        ap.print_help()

if __name__ == "__main__":
    main()