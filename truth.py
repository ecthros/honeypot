import os
import subprocess

for month in range(3,5):
	month = "20160" + str(month)
	for day in range(1,31):
		if(day < 10):
			day = "0" + str(day)
		else:
			day = str(day) 
		time = month + day
		#os.system("echo -n \"Successful Attacks who did not come back ;(:\" >> stats1/" + time)
		#os.system("cat logs1/" + time + " | grep True | cut -d, -f2 | sort | uniq -c | awk '{print $1}' | sort -n | grep -w 1 | wc -l >> stats3/" + time)
		#os.system("echo -n \"Successful Attacks who came back :):\" >> stats1/" + time)
		os.system("echo -n \'=divide(\' >> stats1/" + time)
		os.system("cat logs1/" + time + " | grep True | cut -d, -f2 | sort | uniq -c | awk '{print $1}' | sort -n | grep -vw 1 | wc -l >> stats1/" + time)
		
		
		os.system("perl -pi -e \'chomp if eof\' stats1/" + time)
		os.system("echo -n \', \' >> stats1/" + time)

		os.system("cat logs1/" + time + " | grep True | cut -d, -f2 | sort | uniq | wc -l >> stats1/" + time)
		os.system("perl -pi -e \'chomp if eof\' stats1/" + time)
		os.system("echo \')\' >> stats1/" + time)

# Of all successful attacks, which ones are repeats
