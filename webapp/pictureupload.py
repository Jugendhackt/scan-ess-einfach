#!/usr/bin/python

#---------------------------------------------
#=============================================
#---------------------------------------------
#imports

import csv
#import time as tm
#import numpy as np
import os
import cgi, cgitb

cgitb.enable()

form = cgi.FieldStorage()

#The variables
#httpopen=""
#httpclose=""

#get the fileitem
fileitem=form['userfile']
if fileitem.file:
    #yay...we got a file
    message=fileitem.file.readline()
print """\
Content-Type: text/html\n\n
<html><body>
<p>%s</p>
</body></html>
""" % (message,)
