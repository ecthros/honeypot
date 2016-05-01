#!/bin/python

import os
import subprocess
import time
#as of right now, trigger2 needs to be 1.
def trigger(name): 
	while(True):
		proc = subprocess.Popen(["cat /vz/private/" + str(name) + "/bin/honssh/logs/spoof.log | wc -l"], stdout=subprocess.PIPE, shell=True)
		if(proc.stdout.read()[:-1] != "0"):
			os.system("python /honeypot/recycle.py")
			break
		time.sleep(0.5)
while(True):
	name = "101"
	trigger(name)


