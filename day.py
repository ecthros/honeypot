import os
import subprocess
for i in range(3, 31):
	if(i < 10):
		i = "0" + str(i)
	os.system("cat /101/logs/2016-03-" + str(i) + "*/logs/20* >> logs1/201603" + str(i))

for i in range(1, 30):
        if(i < 10):
                i = "0" + str(i)
        os.system("cat /101/logs/2016-04-" + str(i) + "*/logs/20* >> logs1/201604" + str(i))


for i in range(3, 31):
	if(i < 10):
		i = "0" + str(i)
	os.system("cat /102/logs/2016-03-" + str(i) + "*/logs/20* >> logs2/201603" + str(i))

for i in range(1, 30):
        if(i < 10):
                i = "0" + str(i)
        os.system("cat /102/logs/2016-04-" + str(i) + "*/logs/20* >> logs2/201604" + str(i))


for i in range(3, 31):
	if(i < 10):
		i = "0" + str(i)
	os.system("cat /103/logs/2016-03-" + str(i) + "*/logs/20* >> logs3/201603" + str(i))

for i in range(1, 30):
        if(i < 10):
                i = "0" + str(i)
        os.system("cat /103/logs/2016-04-" + str(i) + "*/logs/20* >> logs3/201604" + str(i))

