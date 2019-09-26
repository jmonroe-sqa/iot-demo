import sys
import os
import socket
import time

hostname = socket.gethostname()
pid = str(os.getpid())

print (pid)
time.sleep(1.5)
