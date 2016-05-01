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
	time = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
	dest = "/" + str(name) + "/logs/" + str(time)
	os.system("mkdir " + dest)
	os.system("cp -r /vz/private/" + str(name) + "/bin/honssh/logs/ " + dest)
	os.system("cp /vz/private/" + str(name) + "/bin/honssh/users.cfg " + dest)
	os.system("cp /vz/private/" + str(name) + "/var/log/password.log " + dest)
	os.system("cp -r /vz/private/" + str(name) + "/bin/honssh/logs/ " + dest)

	#add passwords!
	os.system("cp /vz/private/" + str(name) + "/var/log/auth.log " + dest)
	proc = subprocess.Popen(["cat " + dest + "/password.log | wc -l"], stdout=subprocess.PIPE, shell=True)
	diff = proc.stdout.read() #difference in passwords
	if(diff != str(0)):
	       	with open ("/" + str(name) + "/users.cfg", "r") as myfile:
	            data=myfile.read()
	        data = data[:-1]#remove the last new line character	
		stringToAdd = ""
        	stringToAdd+=data
		toW = '/' + str(name) + '/users.cfg'
        	fileToWrite = open(toW, 'w')
		proc = subprocess.Popen(["cat " + dest + "/password.log"], stdout=subprocess.PIPE, shell=True)
        	passwords = proc.stdout.read().split("\n")
		for password in passwords:
			if(password != "" and password != "\n" and password != "password"):	
				stringToAdd += (", " + password)
		stringToAdd += "\n"
		fileToWrite.write(stringToAdd)
        	fileToWrite.close()

def recycle(name):
	os.system("vzctl stop " + str(name))
	os.system("vzctl destroy " + str(name))
	os.system("vzrestore /media/storage/vzdump" + str(name) + ".tar " + str(name))#Recreate template
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
	if(str(name) == "101"):
		os.system("brctl addif br0 veth" + str(name) + ".0")
 	if(str(name) == "102"):
		os.system("brctl addif br0 veth" + str(name) + ".0")
	os.system("vzctl set " + str(name) + " --nameserver " + gw + " --save")
	os.system("vzctl exec " + str(name) + " service ssh stop")
	os.system("vzctl exec " + str(name) + " service ssh start")
	os.system("cp /" + str(name) + "/users.cfg " + "/vz/private/" + str(name) + "/bin/honssh/users.cfg") #New config, must move to new honeypot.
	os.system("vzctl set " + str(name) + " --userpasswd root:password")
	proc = subprocess.Popen(["vzctl exec " + str(name) + " bash /bin/honssh/start.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

name = "102"
kick(name)
copy(name)
recycle(name)
internet(name)


