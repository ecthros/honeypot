import os
import subprocess
import time
import gdata.spreadsheet.service
import json
from oauth2client.client import SignedJwtAssertionCredentials
import gspread 

json_key = json.load(open('hacs.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)

spread = gc.open_by_key("1QXFTpHJVI79nLunRp8FJFSufMnjTl6NmW1WM7EAiy4c").sheet1

cell = "B2"
startcell=2

os.system("echo \"\" > /home/george/ssh")
os.system("echo \"\" > /home/george/ssh")

while(True):#care: grepping for fbuary as a temporary fix to remove the difference header.
    os.system("cat /var/log/auth.log | grep \"sshd:session): session opened\" | grep -v \"grep\" > /home/george/tmp")
    proc = subprocess.Popen(["diff /home/george/tmp /home/george/ssh | grep \"Feb\""], stdout=subprocess.PIPE, shell=True)
    difference = proc.stdout.read()
    if difference != "":
	entry = spread.update_acell(cell, difference)
	os.system("cat /home/george/tmp > /home/george/ssh")
	startcell = startcell+1
	cell=str("B") + str(startcell)

    os.system("echo \"\" > ~/tmp")
    time.sleep(3)

