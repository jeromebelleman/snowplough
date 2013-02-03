#! /usr/bin/env python

import os, sys
import argparse
from os.path import expanduser, getmtime
import email

def main():
    p = argparse.ArgumentParser()
    p.add_argument('maildir')
    p.add_argument('report')
    args = p.parse_args()

    # Get latest message
    path = args.maildir + '/new/'
    latest = 0
    for e in os.listdir(expanduser(path)):
        if getmtime(path + e) > latest:
            latest = getmtime(path + e)
            mail = path + e

    # Get attachment from message
    # http://stackoverflow.com/questions/4067937
    msg = email.message_from_file(open(mail))
    a = msg.get_payload()[1]
    open(args.report, 'w').write(a.get_payload(decode=True))

if __name__ == '__main__':
    sys.exit(main())
