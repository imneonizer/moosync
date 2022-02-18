#! /usr/bin/python3

import os, sys, json
from .logger import logger
import time
import subprocess as sp
import signal
import socket
from os.path import realpath, dirname, join
from .gpu_stats import gpustats

class MooSync:
    def __init__(self):
        self.config_path = os.path.join(os.path.expanduser('~'), '.moosync.json')
        self.daemon_script = "__moosync.daemon__.py"
    
    def list_background_syncs(self):
        gpustats.pprint()
        
        for pid in sp.check_output("ps aux | awk '/%s/{print $2}'" % self.daemon_script, shell=True).decode().split("\n"):
            try:
                os.kill(int(pid), 0) # mock signal
                print("[+] Daemon PID:", int(pid))
            except (ProcessLookupError, ValueError):
                pass
    
    def stop_background_sync(self, pprint=False):
        if pprint: print("[+] stopping moosync daemon...")
        for pid in sp.check_output("ps aux | awk '/%s/{print $2}'" % self.daemon_script, shell=True).decode().split("\n")[:-1]:
            try:
                os.killpg(int(pid), signal.SIGTERM)
                if pprint: print("[+] killed pid:", int(pid))
            except ProcessLookupError: pass
    
    
    def start_background_sync(self, gpus):
        self.stop_background_sync()
        
        script_path = join(dirname(realpath(__file__)), self.daemon_script) 
        with open("/tmp/moosync_daemon.log", "wb") as null:
            cmd = f"{sys.executable} {script_path} {gpus.strip()}"
            proc = sp.Popen(cmd, shell=True, stdout=null, stderr=null, preexec_fn=os.setsid)
    
    def to_str_format(self, gpus):
        if isinstance(gpus, str):
            gpus = [int(i) for i in gpus.split(",")]
        gpustats.verify_gpu_index(gpus)
        return ','.join([str(i) for i in gpus])
    
    def start(self, args):
        logger.info("syncing gpus")
        
        token = self.get_token()
        if not self.verify_token(token):
            raise RuntimeError("Please login")
        
        gpus = args.gpus.strip().lower()
        
        if  gpus == "all":
            # list all gpus
            # moosync -g all
            gpus = gpustats.all_gpus
    
        elif ":free" in gpus:
            # wait until given gpus are available with memory available more then threshold
            # moosync -g 0,1:free.50
            # moosync -g *:free.50
            
            thresh = 50
            if "." in gpus:
                thresh = int(gpus.split(".")[1])
            
            if gpus.split(":")[0] == "*":
                gpus = gpustats.all_gpus
            else:
                gpus = [int(x) for x in gpus.split(":")[0].split(",")] 
            
            while True:
                # wait until gpus are available
                if gpustats.are_gpus_available(gpus, thresh=thresh/100):
                    break
                time.sleep(1)
        
        elif "free." in gpus:
            # list all gpus with memory available more then threshold
            # moosync -g free.25
            
            free_percent = int(gpus.split("free.")[1])/100
            gpus = gpustats.list_gpus_free_more_than(free_percent)
        
        # verify gpu index and convet list to string
        gpus = self.to_str_format(gpus)
        
        # start background sync process if not already
        self.start_background_sync(gpus)
        return gpus
    
    
    def get_token(self, username=None, password=None, api=None):
        if username and password and api:
            # get token from api
            return "token"
        
        # get token from local storage
        return self.read_config().get('token')
    
    
    def verify_token(self, token):
        return True
    

    def read_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.loads(f.read())
        raise RuntimeError(f"config file '{self.config_path}' not found, please login")
    
    
    def login(self, username, password, api, serial):
        token = self.get_token(username, password, api)
        config = {"token": token, 'serial': serial, 'host': socket.gethostname(), 'api': api}
        
        with open(self.config_path, "w") as f:
            f.write(json.dumps(config))
        
        print(f"[+] Logged in as {username}, config path: {self.config_path}")


moosync = MooSync()
# export CUDA_VISIBLE_DEVICES=$(moosync --gpus 0,1,2)