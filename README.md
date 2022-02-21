## Moosync

A GPU scheduling and collaboration tool.

**Installation Instructions**

- Production

  ````sh
  pip install moosync
  ````

- Development

  ````sh
  python setup.py develop
  ````

**Usage**

Users can get any GPU if they have enough memory available, once selected these GPUs are marked as claimed in the dashboard. Users need to sign up and create profile and then they can authenticate to the server using below command:

````
# login to default server
moosync -t <your-token>

# login to a specific server
moosync -t <your-token> -a http://192.168.0.145:5000
````

- To claim GPUs (return immediately even if they are occupied)

  ````sh
  moosync -g 0,1,2
  ````

- To claim specific GPUs only if they are at least 45% free (wait until they become available)

  ````sh
  moosync -g 0,1,2:free.45
  ````

- To claim all GPUs which are atleast 60% free (wait until they become available)

  ````sh
  moosync -g *:free.45
  ````

- To clear all GPUs (mark them as unoccupied in the dashboard)

  ````sh
  moosync -g clear
  ````

- To clear few GPUs (mark them as unoccupied in the dashboard)

  ````sh
  moosync -g 0,1:clear
  ````

**Additional commands**
- Get logs

  ````sh
  moosync -l
  ````

- List available GPUs and running moosync daemon

  ````sh
  moosync -ls
  ````

- Kill all running GPU sync services in background

  ````sh
  moosync -k
  ````

### Server Setup

coming soon...

