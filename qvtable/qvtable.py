import os
import csv
import time
import imaplib
import email
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATADIR="data"))
app.config.from_envvar('QVTABLE_SETTINGS', silent=True)

datafullpath = os.path.join(app.root_path, app.config.get("DATADIR"))

def email_check():
    '''
    Check email if there are any new messages
    '''
    return
    print("Checking email...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    (retcode, capabilities) = mail.login('example@gmail.com','pass')
    mail.select(readonly=True)
    (retcode, messages) = mail.search(None, '(UNSEEN)')
    if retcode == 'OK':
        for num in messages[0].split():
            print('Processing')
            typ, data = mail.fetch(num,'(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    print(response_part[1])
                    original = email.message_from_string(str(response_part[1]))

                    print (original['From'])
                    print (original['Subject'])
                    typ, data = mail.store(num,'+FLAGS','\\Seen')

@app.route('/')
def show_entries():
    return render_template('main.html')

@app.route('/<filename>')
def show_data(filename):
    filebasename = os.path.basename(filename)
    ffullpath = os.path.join(datafullpath, filebasename)
    if os.path.isfile(ffullpath):
        return render_template('main.html', filename=filebasename)
    return render_template('main.html')

@app.route('/data/')
def get_data_list():
    datafiles = []
    for f in os.listdir(datafullpath):
        ffullpath = os.path.join(datafullpath, f)
        if os.path.isfile(ffullpath):
            filedatestr = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(ffullpath)))
            elem = {"name": f, "date": filedatestr}
            datafiles.append(elem)

    datafilessorted = sorted(datafiles, key=lambda k: k['date'], reverse=True)

    email_check()

    return jsonify(datafilessorted)

@app.route('/data/<filename>')
def get_data(filename):
    # Check if the file exists
    datapath = app.config.get("DATADIR")
    datafilename = os.path.join(datafullpath, os.path.basename(filename))
    if not os.path.exists(datafilename):
        print("Couldn't find file: " + datafilename)
        return None

    # Read the file
    out = []
    with open(datafilename, 'r') as f:
        # Detect the format of the csv file
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        csvreader = csv.reader(f, dialect)
        for row in csvreader:
            out.append(row)

    return jsonify(out)
