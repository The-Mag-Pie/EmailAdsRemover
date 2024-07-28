#!/usr/bin/env python

import os
import poplib, email
from email.header import decode_header
from time import sleep
from datetime import datetime

try:
    POP3_SERVER_ADDR = os.environ["POP3_SERVER_ADDR"]
    LOGIN = os.environ["LOGIN"]
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]
    TIMEOUT_MINUTES = int(os.environ.get("TIMEOUT_MINUTES", 10))
    AD_EMAILS = os.environ["AD_EMAILS"].split(";")
except KeyError as e:
    print(f"Environment variable {e} not set.")
    exit(1)

poplib._MAXLINE = 20480

def connectAndDelete():
    server = poplib.POP3_SSL(POP3_SERVER_ADDR)
    server.user(LOGIN)
    server.pass_(AUTH_TOKEN)

    numOfMessages = len(server.list()[1])

    count = 0

    for i in range(numOfMessages-20, numOfMessages)[::-1]:
        
        raw_email = b"\n".join(server.retr(i+1)[1])
        parsed_email = email.message_from_bytes(raw_email)
            
        try:
            message_from = decode_header(parsed_email["From"])
            message_subject = decode_header(parsed_email["Subject"])
            
            message_from_str = ""
            message_subject_str = ""
            
            for x in message_from:
                if x[1] != None:
                    message_from_str += x[0].decode(x[1])
                else:
                    try:
                        message_from_str += x[0].decode()
                    except:
                        message_from_str += x[0]

            for x in message_subject:
                if x[1] != None:
                    message_subject_str += x[0].decode(x[1])
                else:
                    try:
                        message_subject_str += x[0].decode()
                    except:
                        message_subject_str += x[0]
                    
            start = message_from_str.find("<") + len("<")
            end = message_from_str.find(">")
            message_from_substr = message_from_str[start:end]
            
            if message_from_substr in AD_EMAILS:
                server.dele(i+1)
                print("MESSAGE DELETED:", f"[{message_from_substr}]", message_subject_str)
                count += 1
            
        except:
            print("ERROR")

    server.quit()

    if count == 0:
        print("No messages deleted.\n")
    elif count > 0:
        print(count, " messaged deleted.\n")

while True:
    print(f"[{datetime.now()}] Trying to find and delete ads...")
    try:
        connectAndDelete()
    except Exception as e:
        print(e)
        continue
    sleep(TIMEOUT_MINUTES * 60)
