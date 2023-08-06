import os
from daisyfl.common import PIDS
def shutdown():
    os.system("kill -s 2 $(awk '{print}' " + PIDS + "*.txt)")
