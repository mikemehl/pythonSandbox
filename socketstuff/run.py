import os
from subprocess import Popen

p1 = Popen(['python3', 'server.py'])
p2 = Popen(['python3', 'client.py'])
