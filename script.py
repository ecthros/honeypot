import os
import subprocess
import time
import gdata.spreadsheet.service
import json
from oauth2client.client import SignedJwtAssertionCredentials
import gspread 


def start():
    json_key = json.load(open('hacs.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

    gc = gspread.authorize(credentials)
    return gc

def opened(spread, startcell):
    os.system("cat /var/log/auth.log | grep \"sshd:session): session opened\" | grep -v \"grep\" > /home/george/tmp")
    proc = subprocess.Popen(["diff /home/george/tmp /home/george/ssh | grep \"<\""], stdout=subprocess.PIPE, shell=True)
    difference = proc.stdout.read()
    if difference != "":
        lines = difference.split("\n")
        while len(lines) > 0:
            addline = lines.pop(0)
            if(addline == ""):
                break;
                
            entry = spread.update_acell(str("B")+str(startcell), (addline[:18])[2:])
            pid = addline.split("[")[1].split("]")[0]
            processentry = spread.update_acell(str("C")+str(startcell), pid)
            os.system("echo \"" + str(pid) + ";" + str("E") + str(startcell) + "\" >> /home/george/opened_ssh")
            userentry = spread.update_acell(str("D")+str(startcell), (addline.split("for user ")[1].split(" ")[0]))
            os.system("cat /home/george/tmp > /home/george/ssh")
            startcell = startcell+1

    os.system("echo \"\" > /home/george/tmp")
    return startcell

def closed(spread):
    
    with open ("/home/george/opened_ssh", "r") as myfile:
        data = myfile.read()
    data = data[:-1]
    pids = data.split("\n")

    for i in pids:
        pid = i.split(";")[0]
        proc = subprocess.Popen(["cat /var/log/auth.log | grep \"session closed\" | grep ssh | grep -v grep | grep " + str(pid) + " | wc -l"], stdout = subprocess.PIPE, shell=True)
        lines=proc.stdout.read()[:-1]
        if(lines == str(1)):
            proc = subprocess.Popen(["cat /var/log/auth.log | grep \"session closed\" | grep ssh | grep -v grep | grep " + str(pid)], stdout = subprocess.PIPE, shell=True)
            line = proc.stdout.read()
            entry = str(i.split(";")[1])
            closedentry = spread.update_acell(entry, line[:16])
        elif(lines!=str(0)):
            print str(pid) + "fatal."

def main():
    startcell = 2
    auth = start()
    spread = auth.open_by_key("1QXFTpHJVI79nLunRp8FJFSufMnjTl6NmW1WM7EAiy4c").sheet1
    
    os.system("echo \"\" > /home/george/ssh")
    
    while(True):
        startcell = opened(spread, startcell)
        closed(spread)
        time.sleep(3)

main()


