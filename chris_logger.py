import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import subprocess
from datetime import datetime

json_cred = json.load(open('./creds.json', 'r'))
scope = ['https://spreadsheets.google.com/feeds']


credentials = SignedJwtAssertionCredentials(json_cred['client_email'], json_cred['private_key'], scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_key('1YcI5HBlAofBf5y2p91SdvcKvIxsEdpMmKdVEiuyL09A').worksheet('Health Log')

disk = float(subprocess.check_output("du -s / | tail -1", shell=True).split()[0])/1000000
mem = int(subprocess.check_output("free -m -o | grep Mem | tr -s \  | cut -d\  -f3", shell=True))
cpu = subprocess.check_output("uptime", shell=True)
cpu = cpu.split()



wks.append_row(['Host', datetime.now().strftime("%m/%d/%Y %H:%M:%S"), disk, mem, cpu[7].split(',')[0], cpu[8].split(',')[0], cpu[9], 'N/A'])

for ip in ["101", "102", "103"]:
    disk = float(subprocess.check_output("vzctl exec " + ip + " du -s / | tail -1", shell=True).split()[0])/1000000
    mem = int(subprocess.check_output("vzctl exec " + ip + " free -m -o | grep Mem | tr -s \  | cut -d\  -f3", shell=True))
    cpu = subprocess.check_output("vzctl exec " + ip + " uptime", shell=True)
    cpu = cpu.split()
    date = datetime.now().strftime("%m.%d.%y")

    attacks = 0
    subprocess.check_output("mkdir -p /data/" + ip + "/" + date, shell=True)
    folders = subprocess.check_output("ls /data/" + ip + "/" + date, shell=True).split()
    for time in folders:
        subprocess.check_output("mkdir -p /data/" + ip + "/" + date + "/" + time + "/logs", shell=True)
        #print "cat /data/" + ip + "/" + date + "/" + time + "/logs/* | grep Accepted | wc -l"
        attacks += int(subprocess.check_output("cat /data/" + ip + "/" + date + "/" + time + "/logs/[0-9]*.log | grep Accepted | wc -l", shell=True))

    wks.append_row(["Honeypot " + ip, datetime.now().strftime("%m/%d/%Y %H:%M:%S"), disk, mem, cpu[7].split(',')[0], cpu[8].split(',')[0], cpu[9], attacks])
