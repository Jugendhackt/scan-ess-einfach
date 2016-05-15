#!/usr/bin/python
#-*- coding: UTF-8 -*-
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
                            <p>%s</br><h1>Sonstiges</h1></br>%s</br><hr><img src="%s"></p>
						</footer>
					</section>
				<!-- Footer -->
					<footer id="footer">
						<ul class="copyright">
							<li>&copy; by Team IssEss</li>
							<li>Design: <a href="http://twitter.com/3zscan">by Foz</a></li>
						</ul>
					</footer>
			</div>
	</body>
</html>
""" % (info['product_id'],info['product_name'],info['inhalte'],info['sonstiges'],info['bild'])

def writeerror(info):
    print 'Content-Type: text/html\n\n'
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print """\
<!DOCTYPE HTML>
<html>
        <head>
                <title>Fehler:</title>
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
                                                        </header>
							<h1>Fehler:</h1>
                                                        <br><p>%s</p>
                                                </footer>
                                        </section>
                                <!-- Footer -->
                                        <footer id="footer">
                                                <ul class="copyright">
                                                        <li>&copy; by Team IssEss</li>
                                                        <li>Design: <a href="http://twitter.com/3zscan">by Foz</a></li>
                                                </ul>
                                        </footer>
                        </div>
        </body>
</html>
""" % (info['art'])

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
    pil = pil.resize((1000,1000))
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
    return "---"
    
    

cgitb.enable()

form = cgi.FieldStorage()


#get the fileitem from web user
if form.getvalue('userfile'):
    fileitem=form['userfile']
    #yay...we got a file
    ean="nopicture"
    fn = '/tmp/' + os.path.basename(fileitem.filename)

    if ".png" in fn:
    	open(fn, 'wb').write(fileitem.file.read())
    	ean=decode(fn)
        os.remove(fn)

    if ".jpg" in fn:
	open(fn, 'wb').write(fileitem.file.read())
        ean=decode(fn)
        os.remove(fn)

    if ".JPG" in fn:
        open(fn, 'wb').write(fileitem.file.read())
        ean=decode(fn)
        os.remove(fn)

if form.getvalue('ean'):
    ean=str(form.getvalue('ean'))

if ean == "nopicture":
    info={}
    info['art']="Bitte wähle ein Foto aus!"
    writeerror(info)
    exit()

if ean == "---":
    info={}
    info['art']="Scan fehlgeschlagen, das Foto ist nicht lesbar."
    writeerror(info)
    exit()
	   
data = json.load(urllib2.urlopen('http://world.openfoodfacts.org/api/v0/product/' + ean +'.json'))
find = """/
%s
""" % (data)
find = find.replace(" ", "-")
if "product-found" in find:
		info={}
		info['product_id']=data['product']['code']
		info['inhalte']=data['product']['ingredients_text']
		info['product_name']=data['product']['product_name']
		info['bild']=data['product']['image_front_url']
		info['sonstiges']='Kommt bald...'#fn#data['product']['labels_hierarchy']

		usetztung = csv.reader(open('Uebersetzungstabelle2.csv','rb'))
		for row in usetztung:
    			alt=row[0].decode('utf-8')
    			neu=row[1].decode('utf-8')
    			info['inhalte']=info['inhalte'].replace(alt, neu)
		if form.getvalue('as_json'):
                    writejson(info)
                    exit()
        	else:
                    writehtml(info)
                    exit()    

if "'product-not-found'" in find:
	info={}
	info['art']="Product-ID:<br>" + ean + "<br>Dieses Produkt existiert noch nicht in der Datenbank."
	info['product_id']=ean
	if form.getvalue('as_json'):
            writejson(info)
            exit()
        else:
            writeerror(info)
            exit()
else:
	info={}
	info['art']="Ein Unbekannter Fehler ist aufgetreten!"

	if form.getvalue('as_json'):
    	    writejson(info)
            exit()
	else:
	    writeerror(info)
            exit()
