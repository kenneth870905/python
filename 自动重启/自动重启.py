#encoding:utf-8
import os
import sys
import time
from cacheout import Cache


cache = Cache()
cache = Cache(maxsize=256, ttl=600, timer=time.time, default=None)
# cache.set(1, 'foobar')

ret = cache.get(1)
print(ret)

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    print('ready to restart program......')
    python = sys.executable
    os.execl(python, python, *sys.argv)

# time.sleep(5)

# if os.path.isfile('重启.txt'):
#     restart_program()
