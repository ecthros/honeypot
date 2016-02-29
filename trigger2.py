#!/bin/python

import os
import subprocess

def trigger(name): 
	while(True):
		proc = subprocess.Popen(["vzctl exec " + name + " who"], stdout=subprocess.PIPE, shell=True)
		if(proc.stdout.read() != ""):
			os.system("python /honeypot/recycle2.py")
			break

name = "102"
trigger(name)


