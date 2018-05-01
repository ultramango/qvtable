#!/usr/bin/env python3

import os
import csv
import time
import imaplib
import email
import email.parser

def email_check():
    '''
    Check email if there are any new messages
    '''
    print("Checking email...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    (retcode, capabilities) = mail.login('example@gmail.com','pass')
    mail.select(readonly=True)  # Test mode - will not mark messages as read
    #mail.select()
    (retcode, messages) = mail.search(None, '(UNSEEN)')
    if retcode == 'OK':
        for num in messages[0].split():
            print('Processing')
            typ, data = mail.fetch(num,'(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    #print(response_part[1])
                    msg = email.parser.BytesParser().parsebytes(response_part[1])
                    for part in msg.walk():
                        print("--" + part.get_content_type())
                        print("-- Body: " + part.get_payload(decode=True))
                    b = mgs.get_body()

                    #msg = email.message_from_string(response_part[1])

                    #print("Orig: " + str(msg.items()))

                    print("From: " + msg['From'])
                    print("Subject: " + msg['Subject'])
                    print("Body: " + text)
                    print("OK?")
                    typ, data = mail.store(num,'+FLAGS','\\Seen')
    else:
        print("Retcode did not return OK")

    mail.close()
    mail.logout()

email_check()
