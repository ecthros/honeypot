#!/bin/python

import os
import subprocess
import time

def trigger(name): 
	while(True):
		proc = subprocess.Popen(["cat /vz/private/" + str(name) + "/bin/honssh/logs/spoof.log | wc -l"], stdout=subprocess.PIPE, shell=True)
		if(proc.stdout.read()[:-1] != "0"):
			os.system("python /honeypot/recycle2.py")
			break
		time.sleep(0.5)
while(True):
	name = "102"
	trigger(name)


