#!/bin/python
import os
import subprocess
import time
from time import gmtime, strftime
def kick(name):
	time.sleep(60)
	os.system("vzctl exec " + str(name) + " service ssh stop")
	os.system("vzctl exec " + str(name) + " kill -9 -1")#removes all users.

def copy(name):
	time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	dest = "/" + str(name) + "/logs/honssh" + str(time)
	os.system("mkdir " + dest)
	os.system("cp -r /vz/private/" + str(name) + "/bin/honssh/logs/ " + dest)
	os.system("cp /vz/private/" + str(name) + "/bin/honssh/users.cfg " + dest)
	#add passwords!
	proc = subprocess.Popen(["diff " + dest + "/users.cfg /" + str(name) + "/users.cfg"], stdout=subprocess.PIPE, shell=True)
	diff = proc.stdout.read() #difference in passwords
	if(diff != "" or diff != "\n"):
		proc = subprocess.Popen(["cat " + dest + "/users.cfg | grep fake_passwords"], stdout=subprocess.PIPE, shell=True)
		passwords = proc.stdout.read()
		os.system("head -29 /" + str(name) + "/users.cfg > /" + str(name) + "/tmp") #Takes first 29 lines
		os.system("echo \"" + passwords + "\" >> /" + str(name) + "/tmp")
		os.system("mv /" + str(name) + "/tmp " + "/" + str(name) + "/users.cfg") #New config, must move to new honeypot.
		os.system("cp /" + str(name) + "/users.cfg /vz/private/" + str(name) + "/bin/honssh/users.cfg")
		os.system("rm /" + str(name) + "/tmp")


def recycle(name):
	os.system("vzctl stop " + str(name))
	os.system("vzctl destroy " + str(name))
	os.system("vzctl create " + str(name) + " --ostemplate ubuntu-14.04-x86_64")#Template is named ubuntu
	os.system("vzctl start " + str(name))

def internet(name):
	ip = ""
	netmask = "255.255.255.192"
	gw = "128.8.238.65"
	if(str(name) == "101"):
		ip = "128.8.238.78"
	elif(str(name) == "102"):
		ip = "128.8.238.103"
		

	os.system("vzctl set " + str(name) + " --netif_add eth0 --save")
	os.system("vzctl exec " + str(name) + " ifconfig eth0 " + ip + " netmask " + netmask)
	os.system("vzctl exec " + str(name) + " route add default gw " + gw)
	os.system("brctl addif br0 veth" + str(name) + ".0")
 	os.system("vzctl set " + str(name) + " --nameserver " + gw + " --save")
name = "102"
kick(name)
copy(name)
recycle(name)
internet(name)


