#!/usr/bin/python
#imports
import csv
import os
import cgi, cgitb
from sys import argv
import zbar
import Image
import json
import urllib2
import sys

def writehtml(info):
    print 'Content-Type: text/html\n\n'
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print """\
<!DOCTYPE HTML>
<html>
	<head>
		<title>Auswertung:</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="/assets/css/main.css" />
		<noscript><link rel="stylesheet" href="/assets/css/noscript.css" /></noscript>
	</head>
	<body>

		<!-- Wrapper -->
			<div id="wrapper">

				<!-- Main -->
					<section id="main">
						<header>
							<span class="avatar"><img src="/images/barcode_scanner.png" alt="" /></span>
							<h1>Product-ID</h1>
							<p>%s</br>%s</br></p>
                            <h1>Zutaten</br></h1>
                            <p>%s</p>
						</footer>
					</section>

				<!-- Footer -->
					<footer id="footer">
						<ul class="copyright">
							<li>&copy; by Team IssEss</li>
							<li>Design: <a href="http://twitter.com">by Foz</a></li>
						</ul>
					</footer>

			</div>

	</body>
</html>
""" % (info['product_id'],info['product_name'])

def writejson(info):
    print 'Content-Type: application/json\n\n'
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print json.dumps(info)
    

def decode(f):

    # create a reader
    scanner = zbar.ImageScanner()

    # configure the reader
    scanner.parse_config('enable')

    # obtain image data
    pil = Image.open(f).convert('L')
    width, height = pil.size
    raw = pil.tostring()

    # wrap image data
    image = zbar.Image(width, height, 'GREY', raw)
    # scan the image for barcodes
    scanner.scan(image)

    # extract results
    for symbol in image:
        # do something useful with results
        return symbol.data

    # clean up
    del(image)
    return ".4029764001807"
    
    

cgitb.enable()

form = cgi.FieldStorage()


#get the fileitem from web user
if form.getvalue('userfile'):
    fileitem=form['userfile']
    #yay...we got a file
    fn = '/tmp/' + os.path.basename(fileitem.filename)
    open(fn, 'wb').write(fileitem.file.read())
    ean=decode(fn)
    os.remove(fn)

if form.getvalue('ean'):
    ean=str(form.getvalue('ean'))
    
data = json.load(urllib2.urlopen('http://world.openfoodfacts.org/api/v0/product/' + ean +'.json'))
info={}
info['product_id']=data['product']['code']
info['inhalte']=data['product']['ingredients_text']
info['product_name']=data['product']['product_name']


if form.getvalue('as_json'):
    writejson(info)
else:
    writehtml(info)
