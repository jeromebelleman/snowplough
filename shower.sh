#!/bin/sh

offlineimap -c .offlineimaprc
shovel.py indir report.zip
snowplough mkix report.zip
