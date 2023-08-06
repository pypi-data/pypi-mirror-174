"""
monadic dask

example:
    dasker '{}' python -c "import dasker; print(dasker.get_client().submit(lambda: 'hello, world!').result())"

equivalent example, because it's a monad:
    dasker '{}' dasker '{}' python -c "import dasker; print(dasker.get_client().submit(lambda: 'hello, world!').result())"

if dasker wasn't used to start dask, a default client is used. example:
    python -c "import dasker; print(dasker.get_client().submit(lambda: 'hello, world!').result())"

if you want to override the contextual dask, use --force-new. example:
    dasker '{"processes": false}' dasker --force-new '{"processes": true, "nthreads": 1, "n_workers": 1}' command ... 
"""

from contextlib import contextmanager
import json
import os
import subprocess
import sys


DASK_SCHEDULER = "DASK_SCHEDULER"


def get_client():
    """Get global client using environment variable if possible, otherwise use default"""
    from dask.distributed import Client, get_client
    s = os.getenv(DASK_SCHEDULER)
    print(f"getclient {s}")
    if s is not None:
        return Client(s)
    try:
        c = get_client()
    except ValueError:
        c = Client()
    os.putenv(DASK_SCHEDULER, c.scheduler.address)
    return c


def main():
    forcenew = sys.argv[1] == '--force-new'
    if len(sys.argv) < 3 or (forcenew and len(sys.argv) == 3):
        print("Usage: dasker [--force-new] '{kwargs to distributed.Client}' command")
        return

    s = os.getenv(DASK_SCHEDULER)
    if forcenew or not s:
        from dask.distributed import Client
        client = Client(**json.loads(sys.argv[1 + int(forcenew)]))
        os.putenv(DASK_SCHEDULER, client.scheduler.address)
        print(f"sched {client.scheduler.address}")
    else:
        client = contextmanager(lambda: (yield))()
        
    with client:
        p = subprocess.Popen(sys.argv[2 + int(forcenew) :])
        p.wait()


if __name__ == "__main__":
    main()

