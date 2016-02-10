import os
import subprocess
import time
import gdata.spreadsheet.service
import json
from oauth2client.client import SignedJwtAssertionCredentials
import gspread 
import httplib, urllib

def send(string):
    bot_id = "8de46c22a3fb6c553a4140336f"
    test_id = "a18e6ce0dbb6c106befb5909d4"
    os.system("curl -X POST -d '{\"bot_id\": \"" + test_id + "\", \"text\": \"" + string + "\"}' -H 'Content-Type: application/json' https://api.groupme.com/v3/bots/post")

def start():
    json_key = json.load(open('hacs.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    gc = gspread.authorize(credentials)
    return gc

def deleteLine(string, location):
    fn= location + "opened_ssh"
    f = open(fn)
    output = []
    for line in f:
        if not str(string) in line:
            output.append(line)
    f.close()
    f=open(fn, 'w')
    f.writelines(output)
    f.close()

def opened(spread, startcell, location):
    os.system("cat /var/log/auth.log | grep \"Accepted password\" | grep -v \"grep\" > " + location + "tmp")
    proc = subprocess.Popen(["diff " + location + "tmp " + location + "ssh | grep \"<\""], stdout=subprocess.PIPE, shell=True)
    difference = proc.stdout.read()
    if difference != "":
        lines = difference.split("\n")
        while len(lines) > 0:
            addline = lines.pop(0)
            if(addline == ""):
                break;
                
            entry = spread.update_acell(str("B")+str(startcell), (addline[:8])[2:])
            time = spread.update_acell(str("C")+str(startcell), (addline[:17])[8:])
            pid = addline.split("[")[1].split("]")[0]
            processentry = spread.update_acell(str("D")+str(startcell), pid)
            username = addline.split("password for ")[1].split(" ")[0]
            userentry = spread.update_acell(str("E")+str(startcell), username)
            ip = addline.split("from ")[1].split(" ")[0]
            ipentry = spread.update_acell(str("H")+str(startcell), ip)
            os.system("echo \"" + str(pid) + ";" + str(startcell) + "\" >> " + location + "opened_ssh")
            os.system("cat " + location + "tmp > " + location + "ssh")
            startcell = startcell+1

    os.system("echo \"\" > " + location + "tmp")
    return startcell

def closed(spread, location):
    
    with open (location + "opened_ssh", "r") as myfile:
        data = myfile.read()
    data = data[:-1]
    pids = data.split("\n")
    
    for i in pids:
        if(i!=""):
            pid = i.split(";")[0]
            proc = subprocess.Popen(["cat /var/log/auth.log | grep \"session closed\" | grep ssh | grep -v grep | grep " + str(pid) + " | wc -l"], stdout = subprocess.PIPE, shell=True)
            lines=proc.stdout.read()[:-1]
            if(lines == str(1)):
                proc = subprocess.Popen(["cat /var/log/auth.log | grep \"session closed\" | grep ssh | grep -v grep | grep " + str(pid)], stdout = subprocess.PIPE, shell=True)
                line = proc.stdout.read()
                entry = str(i.split(";")[1])
                closedentry = spread.update_acell(str("F") + entry, line[:6])
                closedtime = spread.update_acell(str("G") + entry, line[:15][6:])
                deleteLine(i, location)
            elif(lines!=str(0)):
                print str(pid) + "fatal."
    
def main():
    
    startcell = 2
    auth = start()
    spread = auth.open_by_key("1QXFTpHJVI79nLunRp8FJFSufMnjTl6NmW1WM7EAiy4c").sheet1
    location = "/home/george/"
    os.system("echo \"\" > " + location + "ssh")
    os.system("echo \"\" > " + location + "opened_ssh")    
    send("Starting....")
    try:
        while(True):
            startcell = opened(spread, startcell, location)
            closed(spread, location)
            time.sleep(3)
    except RuntimeError as e:
        send("SCRIPT ENDING!!" + e.message)


main()


