#!/bin/python
import os
import subprocess
import time

def kick(name):
	time.sleep(60)
	os.system("vzctl exec " + str(name) + " service ssh stop")
	os.system("vzctl exec " + str(name) + " who awk \'!/root/{ cmd=\"/sbin/pkill -KILL -u \" $1; system(cmd)}\'")
	recycle(name)

def recycle(name):
	os.system("vzctl stop " + str(name))
	os.system("vzctl destroy " + str(name))
	os.system("vzctl create " + str(name) + " --ostemplate 102ubuntu")
	#internet stuff
	



