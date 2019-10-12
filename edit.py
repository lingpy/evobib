#!/usr/bin/python2.6
# *-* coding: utf-8 *-*

import cgitb
cgitb.enable()
import cgi
import sqlite3
from collections import defaultdict
import os

# check for remote user
user = os.environ.get('REMOTE_USER', 'unknown')

print "Content-type: text/html; charset=utf-8"

if __file__ == 'edit.py':
    db = sqlite3.connect('data.sqlite3')
else:
    db = sqlite3.connect('data2.sqlite3')

#db = sqlite3.connect('data.sqlite3')
cursor = db.cursor()
cursor.execute('select * from quotes;')
db2 = sqlite3.connect('evobib.sqlite3')
cursor2 = db2.cursor()
cursor2.execute('select key from bibliography;')

version = '1.0'

print ''
print '<head>'
print '<link rel="stylesheet" href="awesomplete.css">'
print '<script src="awesomplete.js"></script>'
print '<link rel="stylesheet" href="style.css">'
print '<script type="text/javascript" src="evobib.py?display=js"></script>'
print '<link rel="icon" href="http://calc.digling.org/img/favicon.png" type="image/png">'
print '<meta name="viewport" content="user-scalable=no,width=device-width,initial-scale=1">'
print '</head>'

# get keywords for js handling
keys, keywords = defaultdict(int), defaultdict(int)
for line in cursor.fetchall():
    keys[line[1]] += 1
    for keyword in line[5].split(','):
        keywords[keyword.strip()] += 1
references = 0
ebdata = []
for key in cursor2.fetchall():
    references += 1
    ebdata += [key[0]]


template = """
<body>
  <style>.comment {{display: {showcomment};}}</style>
  <h1 class="main">EvoBib</h1>
  <h1 class="smart">EvoBib Refs</h1>

  <div class="dropdown">
    <div class="menu-icon">
      <div></div>
      <div></div>
      <div></div>
    </div>
    <div class="dropdown-content">
      <label for="tabreiter-0-0">Welcome</label>
      <label for="tabreiter-0-1">References</label>
      <label for="tabreiter-0-2">Quotes</label>
      <label style="{hidden}" for="tabreiter-0-3">Edit</label>
      <label for="tabreiter-0-4">About</label>
      <label for="tabreiter-0-5">Back2CALC</label>

    </div>
  </div>
  <h2>A Bibliographic Database and Quote Collection</h2>
    <div id="content" class="tabreiter">
      <ul>
	<li class="reiter">
	  <input type="radio" name="tabreiter-0" checked id="tabreiter-0-0" />
	  <label class="main" for="tabreiter-0-0">Welcome</label>
	  <div>
            <div class="base">
              <h3>Welcome to EvoBib</h3>
<p>
<svg style="width:300px;float:right;" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" id="svg2" version="1.1" inkscape:version="0.48.4 r9939" viewBox="0 0 510 380" xml:space="preserve" sodipodi:docname="evobib.svg"><metadata id="metadata8"><rdf:rdf><cc:work rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"></dc:type><dc:title></dc:title></cc:work></rdf:rdf></metadata><defs id="defs6"><clipPath clipPathUnits="userSpaceOnUse" id="clipPath20"><path d="m 0,0 2384,0 0,3370 L 0,3370 0,0 z" id="path22" inkscape:connector-curvature="0"></path></clipPath><clipPath clipPathUnits="userSpaceOnUse" id="clipPath34"><path d="m 0,0 2384,0 0,3370 L 0,3370 0,0 z" id="path36" inkscape:connector-curvature="0"></path></clipPath><clipPath clipPathUnits="userSpaceOnUse" id="clipPath108"><path d="m 0,0 2384,0 0,3370 L 0,3370 0,0 z" id="path110" inkscape:connector-curvature="0"></path></clipPath><clipPath clipPathUnits="userSpaceOnUse" id="clipPath122"><path d="m 0,0 2384,0 0,3370 L 0,3370 0,0 z" id="path124" inkscape:connector-curvature="0"></path></clipPath></defs><sodipodi:namedview pagecolor="#ffffff" bordercolor="#666666" borderopacity="1" objecttolerance="10" gridtolerance="10" guidetolerance="10" inkscape:pageopacity="0" inkscape:pageshadow="2" inkscape:window-width="1920" inkscape:window-height="1000" id="namedview4" showgrid="false" inkscape:zoom="1.17742" inkscape:cx="42.306957" inkscape:cy="161.18761" inkscape:window-x="0" inkscape:window-y="49" inkscape:window-maximized="1" inkscape:current-layer="g130"></sodipodi:namedview><g id="g10" inkscape:groupmode="layer" inkscape:label="buch_evobib" transform="matrix(1.25,0,0,-1.25,0,380.00001)"><g id="g12" transform="translate(72,154.77)"><g id="g14" transform="matrix(1.7001343,0,0,1.7001343,-117.67374,-191.93443)"><g id="g16"><g id="g18" clip-path="url(#clipPath20)"><g id="g24" transform="scale(0.229721,0.229721)"><path d="m 698.383,347.969 c 0,-33.196 -99.09,-33.196 -99.09,0" style="fill:none;stroke:#000000;stroke-width:3.64278293;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path26" inkscape:connector-curvature="0"></path></g></g></g></g><g id="g28" transform="matrix(1.7001343,0,0,1.7001343,-117.67374,-191.93443)"><g id="g30"><g id="g32" clip-path="url(#clipPath34)"><g id="g38" transform="scale(0.229721,0.229721)"><path d="m 698.383,595.688 c 0,-33.196 -99.09,-33.196 -99.09,0" style="fill:none;stroke:#000000;stroke-width:3.64278293;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path40" inkscape:connector-curvature="0"></path><path d="m 637.402,494.562 0,368.454 490.108,0 0,-736.903 -490.108,0" style="fill:#fffacd;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path42" inkscape:connector-curvature="0"></path><path d="m 637.402,494.562 0,368.454 490.108,0 0,-736.903 -490.108,0 0,368.449 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path44" inkscape:connector-curvature="0"></path><path d="m 683.289,371.168 c 0,5.855 -4.75,10.605 -10.605,10.605 -5.856,0 -10.606,-4.75 -10.606,-10.605 0,-5.856 4.75,-10.606 10.606,-10.606 5.855,0 10.605,4.75 10.605,10.606" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path46" inkscape:connector-curvature="0"></path><path d="m 683.289,371.168 c 0,5.855 -4.75,10.605 -10.605,10.605 -5.856,0 -10.606,-4.75 -10.606,-10.605 0,-5.856 4.75,-10.606 10.606,-10.606 5.855,0 10.605,4.75 10.605,10.606 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path48" inkscape:connector-curvature="0"></path><path d="m 683.289,617.957 c 0,5.855 -4.75,10.605 -10.605,10.605 -5.856,0 -10.606,-4.75 -10.606,-10.605 0,-5.855 4.75,-10.605 10.606,-10.605 5.855,0 10.605,4.75 10.605,10.605" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path50" inkscape:connector-curvature="0"></path><path d="m 683.289,617.957 c 0,5.855 -4.75,10.605 -10.605,10.605 -5.856,0 -10.606,-4.75 -10.606,-10.605 0,-5.855 4.75,-10.605 10.606,-10.605 5.855,0 10.605,4.75 10.605,10.605 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path52" inkscape:connector-curvature="0"></path><path d="m 649.742,482.223 0,368.453 490.108,0 0,-736.903 -490.108,0" style="fill:#fffacd;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path54" inkscape:connector-curvature="0"></path><path d="m 649.742,482.223 0,368.453 490.108,0 0,-736.903 -490.108,0 0,368.45 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path56" inkscape:connector-curvature="0"></path><path d="m 695.629,358.828 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path58" inkscape:connector-curvature="0"></path><path d="m 695.629,358.828 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path60" inkscape:connector-curvature="0"></path><path d="m 695.629,605.621 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path62" inkscape:connector-curvature="0"></path><path d="m 695.629,605.621 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path64" inkscape:connector-curvature="0"></path><path d="m 662.078,469.883 0,368.453 490.112,0 0,-736.902 -490.112,0" style="fill:#fffacd;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path66" inkscape:connector-curvature="0"></path><path d="m 662.078,469.883 0,368.453 490.112,0 0,-736.902 -490.112,0 0,368.449 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path68" inkscape:connector-curvature="0"></path><path d="m 707.969,346.488 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path70" inkscape:connector-curvature="0"></path><path d="m 707.969,346.488 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path72" inkscape:connector-curvature="0"></path><path d="m 707.969,593.281 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path74" inkscape:connector-curvature="0"></path><path d="m 707.969,593.281 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path76" inkscape:connector-curvature="0"></path><path d="m 131.48,482.223 0,368.453 490.114,0 0,-736.903 -490.114,0" style="fill:#fffacd;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path78" inkscape:connector-curvature="0"></path><path d="m 131.48,482.223 0,368.453 490.114,0 0,-736.903 -490.114,0 0,368.45 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path80" inkscape:connector-curvature="0"></path><path d="m 596.914,358.828 c 0,5.856 -4.75,10.606 -10.605,10.606 -5.856,0 -10.606,-4.75 -10.606,-10.606 0,-5.855 4.75,-10.605 10.606,-10.605 5.855,0 10.605,4.75 10.605,10.605" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path82" inkscape:connector-curvature="0"></path><path d="m 596.914,358.828 c 0,5.856 -4.75,10.606 -10.605,10.606 -5.856,0 -10.606,-4.75 -10.606,-10.606 0,-5.855 4.75,-10.605 10.606,-10.605 5.855,0 10.605,4.75 10.605,10.605 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path84" inkscape:connector-curvature="0"></path><path d="m 596.914,605.621 c 0,5.856 -4.75,10.606 -10.605,10.606 -5.856,0 -10.606,-4.75 -10.606,-10.606 0,-5.855 4.75,-10.605 10.606,-10.605 5.855,0 10.605,4.75 10.605,10.605" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path86" inkscape:connector-curvature="0"></path><path d="m 596.914,605.621 c 0,5.856 -4.75,10.606 -10.605,10.606 -5.856,0 -10.606,-4.75 -10.606,-10.606 0,-5.855 4.75,-10.605 10.606,-10.605 5.855,0 10.605,4.75 10.605,10.605 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path88" inkscape:connector-curvature="0"></path><path d="m 143.82,469.883 0,368.453 490.11,0 0,-736.902 -490.11,0" style="fill:#fffacd;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path90" inkscape:connector-curvature="0"></path><path d="m 143.82,469.883 0,368.453 490.11,0 0,-736.902 -490.11,0 0,368.449 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path92" inkscape:connector-curvature="0"></path><path d="m 609.254,346.488 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path94" inkscape:connector-curvature="0"></path><path d="m 609.254,346.488 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path96" inkscape:connector-curvature="0"></path><path d="m 609.254,593.281 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605" style="fill:#bfbfbf;fill-opacity:1;fill-rule:nonzero;stroke:none" id="path98" inkscape:connector-curvature="0"></path><path d="m 609.254,593.281 c 0,5.856 -4.75,10.606 -10.606,10.606 -5.855,0 -10.605,-4.75 -10.605,-10.606 0,-5.855 4.75,-10.605 10.605,-10.605 5.856,0 10.606,4.75 10.606,10.605 z" style="fill:none;stroke:#000000;stroke-width:2.0407095;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path100" inkscape:connector-curvature="0"></path></g></g></g></g><g id="g102" transform="matrix(1.7001343,0,0,1.7001343,-117.67374,-191.93443)"><g id="g104"><g id="g106" clip-path="url(#clipPath108)"><g id="g112" transform="scale(0.229721,0.229721)"><path d="m 698.383,347.969 c 0,-33.196 -99.09,-33.196 -99.09,0" style="fill:none;stroke:#000000;stroke-width:3.64278293;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path114" inkscape:connector-curvature="0"></path></g></g></g></g><g id="g116" transform="matrix(1.7001343,0,0,1.7001343,-117.67374,-191.93443)"><g id="g118"><g id="g120" clip-path="url(#clipPath122)"><g id="g126" transform="scale(0.229721,0.229721)"><path d="m 698.383,595.688 c 0,-33.196 -99.09,-33.196 -99.09,0" style="fill:none;stroke:#000000;stroke-width:3.64278293;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none" id="path128" inkscape:connector-curvature="0"></path></g></g></g></g><g id="g130" transform="matrix(0.5,0.866,-0.866,0.5,-34.72,-33.52)"><text transform="scale(1,-1)" id="text132" x="71.467873" y="56.534645" style="font-size:20.40161133px"><tspan style="font-size:60.6879921px;font-variant:normal;font-weight:bold;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa-Bold" x="71.467873 71.467873 71.467873 114.37428 132.76273" y="56.534645 56.534645" sodipodi:role="line" id="tspan134"> B ib</tspan></text>
<g id="g136" transform="matrix(0.5,-0.866,0.866,0.5,46.39,-13.31)"><g id="g138" transform="matrix(0.9192626,0,0,0.9192626,81.651226,33.114599)"><text transform="matrix(1,0,0,-1,108.06,69.32)" id="text140"><tspan style="font-size:20.66300011px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 13.534265 19.257915 32.792179 38.970417 44.694069 58.145683 72.692436 83.561172 95.049797 108.58407 119.70076" y="0" sodipodi:role="line" id="tspan142">Bibliography</tspan></text>
<text transform="matrix(1,0,0,-1,111.8,30.4)" id="text144"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.4117641 8.0344324 11.137014 14.353178 18.244856 21.389284" y="0" sodipodi:role="line" id="tspan146">Author,</tspan></text>
<text transform="matrix(1,0,0,-1,143.18,30.4)" id="text148"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 19.78718 23.678858 28.293875 31.665466 35.03706 38.408649 42.210659 47.387608 52.361301 55.577465 62.039684 66.451447 70.07412 73.176697 76.39286 80.284538 86.20874 90.100418 96.610458 99.713043 102.92921" y="0" sodipodi:role="line" id="tspan150">Name(2000):TheAuthorofthe</tspan><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 17.013388 24.133186 28.54495 32.167618 35.270199 38.486362 42.37804 45.522469 51.787415 56.743176 60.066944 65.112373 68.800804" y="6.9699998" sodipodi:role="line" id="tspan152">Name.Author:Name.</tspan></text>
<text transform="matrix(1,0,0,-1,111.8,4.5)" id="text154"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.4117641 8.0344324 11.137014 14.353178 18.244856 21.389284" y="0" sodipodi:role="line" id="tspan156">Author,</tspan></text>
<text transform="matrix(1,0,0,-1,143.18,4.5)" id="text158"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 19.78718 23.678858 28.293875 31.665466 35.03706 38.408649 42.210659 47.387608 52.361301 55.577465 62.039684 66.451447 70.07412 73.176697 76.39286 80.284538 86.20874 90.100418 96.610458 99.713043 102.92921" y="0" sodipodi:role="line" id="tspan160">Name(2000):TheAuthorofthe</tspan><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 17.013388 24.133186 28.54495 32.167618 35.270199 38.486362 42.37804 45.522469 51.787415 56.743176 60.066944 65.112373 68.800804" y="6.9699998" sodipodi:role="line" id="tspan162">Name.Author:Name.</tspan></text>
<text transform="matrix(1,0,0,-1,111.8,-21.4)" id="text164"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.4117641 8.0344324 11.137014 14.353178 18.244856 21.389284" y="0" sodipodi:role="line" id="tspan166">Author,</tspan></text>
<text transform="matrix(1,0,0,-1,143.18,-21.4)" id="text168"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 19.78718 23.678858 28.293875 31.665466 35.03706 38.408649 42.210659 47.387608 52.361301 55.577465 62.039684 66.451447 70.07412 73.176697 76.39286 80.284538 86.20874 90.100418 96.610458 99.713043 102.92921" y="0" sodipodi:role="line" id="tspan170">Name(2000):TheAuthorofthe</tspan><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 17.013388 24.133186 28.54495 32.167618 35.270199 38.486362 42.37804 45.522469 51.787415 56.743176 60.066944 65.112373 68.800804" y="6.98" sodipodi:role="line" id="tspan172">Name.Author:Name.</tspan></text>
<text transform="matrix(1,0,0,-1,111.8,-47.31)" id="text174"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.4117641 8.0344324 11.137014 14.353178 18.244856 21.389284" y="0" sodipodi:role="line" id="tspan176">Author,</tspan></text>
<text transform="matrix(1,0,0,-1,143.18,-47.31)" id="text178"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 19.78718 23.678858 28.293875 31.665466 35.03706 38.408649 42.210659 47.387608 52.361301 55.577465 62.039684 66.451447 70.07412 73.176697 76.39286 80.284538 86.20874 90.100418 96.610458 99.713043 102.92921" y="0" sodipodi:role="line" id="tspan180">Name(2000):TheAuthorofthe</tspan><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 17.013388 24.133186 28.54495 32.167618 35.270199 38.486362 42.37804 45.522469 51.787415 56.743176 60.066944 65.112373 68.800804" y="6.9699998" sodipodi:role="line" id="tspan182">Name.Author:Name.</tspan></text>
<text transform="matrix(1,0,0,-1,111.8,-73.21)" id="text184"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.4117641 8.0344324 11.137014 14.353178 18.244856 21.389284" y="0" sodipodi:role="line" id="tspan186">Author,</tspan></text>
<text transform="matrix(1,0,0,-1,143.18,-73.21)" id="text188"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 19.78718 23.678858 28.293875 31.665466 35.03706 38.408649 42.210659 47.387608 52.361301 55.577465 62.039684 66.451447 70.07412 73.176697 76.39286 80.284538 86.20874 90.100418 96.610458 99.713043 102.92921" y="0" sodipodi:role="line" id="tspan190">Name(2000):TheAuthorofthe</tspan><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 17.013388 24.133186 28.54495 32.167618 35.270199 38.486362 42.37804 45.522469 51.787415 56.743176 60.066944 65.112373 68.800804" y="6.9699998" sodipodi:role="line" id="tspan192">Name.Author:Name.</tspan></text>
<text transform="matrix(1,0,0,-1,111.8,-99.11)" id="text194"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.4117641 8.0344324 11.137014 14.353178 18.244856 21.389284" y="0" sodipodi:role="line" id="tspan196">Author,</tspan></text>
<text transform="matrix(1,0,0,-1,143.18,-99.11)" id="text198"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 19.78718 23.678858 28.293875 31.665466 35.03706 38.408649 42.210659 47.387608 52.361301 55.577465 62.039684 66.451447 70.07412 73.176697 76.39286 80.284538 86.20874 90.100418 96.610458 99.713043 102.92921" y="0" sodipodi:role="line" id="tspan200">Name(2000):TheAuthorofthe</tspan><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 17.013388 24.133186 28.54495 32.167618 35.270199 38.486362 42.37804 45.522469 51.787415 56.743176 60.066944 65.112373 68.800804" y="6.98" sodipodi:role="line" id="tspan202">Name.Author:Name.</tspan></text>
<text transform="matrix(1,0,0,-1,111.8,-125.01)" id="text204"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.4117641 8.0344324 11.137014 14.353178 18.244856 21.389284" y="0" sodipodi:role="line" id="tspan206">Author,</tspan></text>
<text transform="matrix(1,0,0,-1,143.18,-125.01)" id="text208"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 19.78718 23.678858 28.293875 31.665466 35.03706 38.408649 42.210659 47.387608 52.361301 55.577465 62.039684 66.451447 70.07412 73.176697 76.39286 80.284538 86.20874 90.100418 96.610458 99.713043 102.92921" y="0" sodipodi:role="line" id="tspan210">Name(2000):TheAuthorofthe</tspan><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 17.013388 24.133186 28.54495 32.167618 35.270199 38.486362 42.37804 45.522469 51.787415 56.743176 60.066944 65.112373 68.800804" y="6.98" sodipodi:role="line" id="tspan212">Name.Author:Name.</tspan></text>
<text transform="matrix(1,0,0,-1,111.8,-150.92)" id="text214"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.4117641 8.0344324 11.137014 14.353178 18.244856 21.389284" y="0" sodipodi:role="line" id="tspan216">Author,</tspan></text>
<text transform="matrix(1,0,0,-1,143.18,-150.92)" id="text218"><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 19.78718 23.678858 28.293875 31.665466 35.03706 38.408649 42.210659 47.387608 52.361301 55.577465 62.039684 66.451447 70.07412 73.176697 76.39286 80.284538 86.20874 90.100418 96.610458 99.713043 102.92921" y="0" sodipodi:role="line" id="tspan220">Name(2000):TheAuthorofthe</tspan><tspan style="font-size:5.97800016px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa" x="0 4.9557619 8.2795296 13.324962 17.013388 24.133186 28.54495 32.167618 35.270199 38.486362 42.37804 45.522469 51.787415 56.743176 60.066944 65.112373 68.800804" y="6.9699998" sodipodi:role="line" id="tspan222">Name.Author:Name.</tspan></text>
</g></g></g><text transform="matrix(0.500011,0.86601905,0.86601905,-0.500011,0,0)" id="text132-3" x="-103.6588" y="53.162853" style="font-size:20.4011631px"><tspan style="font-size:60.68665695px;font-variant:normal;font-weight:bold;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa-Bold" x="-103.6588 -103.6588 -103.6588 -42.365284" y="53.162853" sodipodi:role="line" id="tspan134-7"> E </tspan></text>
<text transform="matrix(0.50001101,0.86601905,0.86601905,-0.50001101,0,0)" id="text132-3-2" x="-67.224144" y="49.088348" style="font-size:20.4011631px"><tspan style="font-size:60.68665695px;font-variant:normal;font-weight:bold;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa-Bold" x="-67.224144 -67.224144 -67.224144 -5.9306426" sodipodi:role="line" id="tspan134-7-8">v</tspan></text>
<text transform="matrix(0.50001101,0.86601905,0.86601905,-0.50001101,0,0)" id="text132-3-8" x="-26.549919" y="42.080326" style="font-size:20.4011631px"><tspan style="font-size:60.68665695px;font-variant:normal;font-weight:bold;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:Purisa;-inkscape-font-specification:Purisa-Bold" x="-26.549919 -26.549919 -26.549919 34.743584" sodipodi:role="line" id="tspan134-7-2">o</tspan></text>
</g></g></svg>

              This databases offers {references} references dealing with
              computer-assisted language comparison in a broad sense. In
              addition, the database offers {quotes} distinct quotes collected from
              {refs} references. The majority of the references in the quote database
              overlaps with those in the bibliographic database. 
              The quotes are organized by keywords and
              can browsed with a full text and a keyword search. 
              </p>
              <p>
              The data (references and quotes) underlying each new
              release can also be downloaded from <a
              href="https://zenodo.org">Zenodo</a>.
</p>
<p>
<table>
<tr>
<th style="background-color:#ffa600;width:100px">Release:</th>
<td> {version}</td></tr><tr>
<th style="background-color:#ffa600;width:100px">Date</th>
<td> October 12, 2019</td></tr><tr>
<th style="background-color:#ffa600;width:100px">DOI:</th>
<td>
<a href="https://doi.org/10.5281/zenodo.3302056"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3302056.svg" alt="DOI"></a>
</td></tr><tr>

<th style="background-color:#ffa600;width:100px">Author:</th>
<td> Johann-Mattis List</td></tr>
</table>

            </div>
            {footer}
	  </div>
	</li>
	<li class="reiter">
	  <input type="radio" name="tabreiter-0" id="tabreiter-0-1" />
	  <label class="main" for="tabreiter-0-1">References</label>
	  <div>
	    <div class="base">
              <h3 id="fill_references">Browse {references} References</h3>
              <input id="e_key" onkeyup="checkloade(event)" placeholder="bibtex key" class="ipt awesomplete" data-list="{ebdata}" type="text" name="keye" value=""/>
              <input id="e_phrase" onkeyup="checkloade(event)" placeholder="phrase" class="ipt awesomplete" type="text" name="phrasee" value=""/>
              <input type="button" value="Submit" onclick="loade()" />
              <div id="queriese" style="padding-top:10px;">
                No values selected.
              </div>
	    </div>
          {footer}
          </div>
	</li>
	<li class="reiter">
	  <input type="radio" name="tabreiter-0" id="tabreiter-0-2" />
	  <label class="main" for="tabreiter-0-2">Quotes</label>
	  <div>
	    <div class="base">
              <h3>Browse {quotes} Quotes in {refs} References</h3>
              <input id="q_idf" type="hidden" value=""/>
              <input id="q_key" onsubmit="load()" placeholder="bibtex key" class="ipt awesomplete" data-list="{ac_keys}" type="text" name="key" value=""/>
              <input id="q_phrase" onsubmit="load()" placeholder="phrase" class="ipt awesomplete" type="text" name="phrase" value=""/>
              <input id="q_keyword" onsubmit="load()" placeholder="keyword" class="ipt awesomplete" data-multiple data-list="{ac_kws}" type="text" name="keyword" value=""/>
              <input type="button" value="Submit" onclick="load()" />
              <div id="queries" style="padding-top:10px;">
                No values selected.
              </div>
	    </div>
          {footer}
          </div>
	</li>
        <li class="reiter" style="{hidden}">
	  <input type="radio" name="tabreiter-0" id="tabreiter-0-3" />
	  <label class="main" for="tabreiter-0-3">Edit</label>
	  <div>
            <div class="base">
              <h3>Edit References</h3>
              <span id="feedback"></span>
              <input id="a_key" type="text" class="ipt awesomplete" data-list="{ac_keys}" placeholder="bibtexkey" value="" name="key" />
              <input id="a_page" type="text" class="ipt" placeholder="page" name="page" value="" />
              <br>
              <textarea id="a_phrase" rows="10" cols="40" name="quote" placeholder="write your quote here"/></textarea><br>
              <input id="a_comment" type="text" class="ipt" placeholder="comment" name="note" value="" />
              <input id="a_keyword" value="" type="text" data-multiple-d data-list="{ac_kws}" class="ipt awesomplete" placeholder="keywords" name="keywords" />
              <input type="submit" value="OK" onclick="add();" />
	    </div>
          {footer}
          </div>
	</li>
	<li class="reiter">
	  <input type="radio" name="tabreiter-0" id="tabreiter-0-4" />
	  <label class="main" for="tabreiter-0-4">About</label>
	  <div><div class="base">
      <h3>About the Reference Browser</h3>
      <p>
              This is a collection of references, collected as part of my
              research since 2014. The references are ordered by bibliographic
              keys, which correspond to the keys assigned by the 
              <a href="http://bibliography.lingpy.org">EvoBib</a> bibliography,
              and further annotated by adding inline comments, external
              comments, page range, as well as a selection of keywords.
              The tool was intended to serve as some kind of an &quot;external
              brain&quot; in my research, as it turned out that I could no longer
              keep up with all the references I read, and I had to organize
              myself more properly in order to be able to keep track with the
              large amount of literature that I encountered in daily research.
              As of now, the data contains as many as {quotes} distinct quotes
              distributed across {refs} references.
              </p>
        <p>
              I decided to share these quotes publicly when I realized that it
              was useful in communication with colleagues to be able to point
              to a quick quote that would illustrate a given point. I think it
              is needless to say that in using this reference browser as a
              research tool, one should make sure to really read and check with the
              references collected so far. 
        </p><p>

              In the future I plan to further extent the tool, so that other
              colleagues could join in and add their own quotes. For the time
              being, however, I still test the tool with myself as only editor,
              to make sure it works easy enough to edit data in this fashion
              and to display it on the web.
      </p>

	  </div>
          {footer}
          </div>
	</li>
	<li class="reiter">
	  <input type="radio" name="tabreiter-0" id="tabreiter-0-5" />
	  <label class="main" for="tabreiter-0-5" onclick="window.location.href
          = 'http://calc.digling.org';">Back2CALC</label>	  
	</li>
      </ul>
    </div>
  <script>
new Awesomplete('input[data-multiple]', {{
	filter: function(text, input) {{
		return Awesomplete.FILTER_CONTAINS(text, input.match(/[^,]*$/)[0]);
	}},

	item: function(text, input) {{
		return Awesomplete.ITEM(text, input.match(/[^,]*$/)[0]);
	}},

	replace: function(text) {{
		var before = this.input.value.match(/^.+,\s*|/)[0];
		this.input.value = before + text + ", ";
	}}
}});
new Awesomplete('input[data-multiple-d]', {{
	filter: function(text, input) {{
		return Awesomplete.FILTER_CONTAINS(text, input.match(/[^,]*$/)[0]);
	}},

	item: function(text, input) {{
		return Awesomplete.ITEM(text, input.match(/[^,]*$/)[0]);
	}},

	replace: function(text) {{
		var before = this.input.value.match(/^.+,\s*|/)[0];
		this.input.value = before + text + ", ";
	}}
}});

// Get the input field
var i, inputs, input;
inputs = ['q_key', 'q_phrase', 'q_keyword'];
for (i=0; i<inputs.length; i++) {{
  input = document.getElementById(inputs[i]);

  // Execute a function when the user releases a key on the keyboard
  input.addEventListener("keyup", function(event) {{
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {{
      load();
    }}
  }});
}}

function loade() {{
  var key, phrase, ebs, eb, i;
  key = document.getElementById('e_key').value;
  phrase = document.getElementById('e_phrase').value;

  var xhr = new XMLHttpRequest();
  if (key != '') {{
    xhr.open(
      'GET',
      'evobib.py?display=table&keys='+key
      );
  }}
  else if (phrase != '') {{
    xhr.open(
      'GET',
      'evobib.py?display=table&search='+phrase
    );
  }}
  xhr.onload = function() {{
    if (xhr.status === 200) {{
      document.getElementById('queriese').innerHTML = xhr.responseText;
      ebs = document.getElementsByClassName('ebkey');
      for (i=0; i<ebs.length; i++) {{
        eb = ebs[i];
        if ("{evoref}".indexOf(eb.dataset.eb) != -1) {{
          eb.style.color = 'Crimson';
          eb.style.cursor = 'pointer';
          eb.onclick = function(){{
            document.getElementById('q_key').value = this.dataset.eb;
            load();
            document.getElementById('tabreiter-0-2').checked='checked';
          }}
        }}
        else {{
          eb.style.color = 'black';
        }}
      }}
    }}
    else {{
        alert('Request failed.  Returned status of ' + xhr.status);
    }}
  }};
  xhr.send();
}}


function load() {{
  var idf, key, phrase, keyword, i, eb;
  idf = document.getElementById('q_idf').value;
  key = document.getElementById('q_key').value;
  phrase = document.getElementById('q_phrase').value;
  keyword = document.getElementById('q_keyword').value;

  var xhr = new XMLHttpRequest();
  if (idf != '') {{
    xhr.open(
      'GET',
      'query.py?show=yes&idf='+idf+'&user={user}'
      );
    document.getElementById('q_idf').value = '';
  }}
  else {{
    xhr.open(
      'GET',
      'query.py?show=yes&key='+key+'&phrase='+phrase+'&keyword='+keyword+'&user={user}'
    );
  }}
  xhr.onload = function() {{
    if (xhr.status === 200) {{
      document.getElementById('queries').innerHTML = xhr.responseText;
      ebs = document.getElementsByClassName('eb');
      for (i=0; i<ebs.length; i++) {{
        eb = ebs[i];
        if (typeof EvoBib[eb.dataset['eb']] == 'undefined') {{
          eb.innerHTML = '';
        }}
        else {{
          eb.style.color = 'Crimson';
        }}
      }}
    }}
    else {{
        alert('Request failed.  Returned status of ' + xhr.status);
    }}
  }};
  xhr.send();
}}
function add() {{
  var key, page, phrase, comment, keyword;
  key = document.getElementById('a_key');
  page = document.getElementById('a_page');
  phrase = document.getElementById('a_phrase');
  comment = document.getElementById('a_comment');
  keyword = document.getElementById('a_keyword');
  
  var xhr = new XMLHttpRequest();
  xhr.open(
    'GET',
    'update.py?add=yes&key=' 
      + encodeURIComponent(key.value)+'&phrase=' 
      + encodeURIComponent(phrase.value)+'&keyword='
      + encodeURIComponent(keyword.value)+'&page='
      + encodeURIComponent(page.value)+'&comment='
      + encodeURIComponent(comment.value)
  );
  xhr.onload = function() {{
    if (xhr.status === 200) {{
      if (xhr.responseText.indexOf('success') != -1) {{
        page.value = '';
        phrase.value = '';
        comment.value = '';
        keyword.value = '';
      }}
      else {{
        document.getElementById('feedback').innerHTML = xhr.responseText;
      }}
    }}
    else {{
      alert('Request failed.');
    }}
  }};
  xhr.send();
}}

function loadIDF(node, idf) {{
  var el, quote, keywords, comment, tds;
  var xhr = new XMLHttpRequest();
  node.value = 'Modify';
  node.onclick = function (){{prepareModification(node)}};
  xhr.open(
    'GET',
    'query.py?show=yes&idf='+idf+'&user={user}'
  );
  xhr.onload = function() {{
    if (xhr.status === 200) {{
      el = document.createElement('html');
      el.innerHTML = xhr.responseText;
      tds = el.getElementsByTagName('td');
      document.getElementById(idf+'_quote').innerHTML = tds[0].innerHTML; 
      document.getElementById(idf+'_keywords').innerHTML = tds[2].innerHTML; 
      document.getElementById(idf+'_comment').innerHTML = tds[1].innerHTML; 
    }}
    else {{
        alert('Request failed.  Returned status of ' + xhr.status);
    }}
  }};
  xhr.send();
}}

function prepareModification(node) {{
  var quote, comment, keywords, idf;
  idf = node.dataset['idf'];
  quote = document.getElementById(node.dataset['idf']+'_quote');
  comment = document.getElementById(node.dataset['idf']+'_comment');
  keywords = document.getElementById(node.dataset['idf']+'_keywords');
    
  quote.innerHTML = '<textarea id="'+ idf +
    '_m_quote">'+node.dataset['quote'] +
    '</textarea><br><input id="' + 
    idf + '_m_page" type="text" value="'+node.dataset['page'] + '"/>' +
    '<input id="' + idf +'_m_key'+'" type="text" value="'+node.dataset['key']+'"/>';
  comment.innerHTML = '<input id="' + idf + 
    '_m_comment" type="text" value="'+node.dataset['note']+'" />';
  keywords.innerHTML = '<input id="' + idf + 
    '_m_keywords" type="text" value="'+node.dataset['keywords']+'" />';

  node.value = 'Submit';
  node.onclick = function (){{modify(node, idf)}};
}}

function modify(node, idf) {{
  var key, page, phrase, comment, keyword, ebs, i, eb;
  key = document.getElementById(idf+'_m_key');
  page = document.getElementById(idf+'_m_page');
  phrase = document.getElementById(idf+'_m_quote');
  comment = document.getElementById(idf+'_m_comment');
  keyword = document.getElementById(idf+'_m_keywords');
  node.dataset['keywords'] = keyword.value;
  node.dataset['note'] = comment.value;
  node.dataset['quote'] = phrase.value;
  node.dataset['page'] = page.value;
  node.dataset['key'] = key.value;

  var xhr = new XMLHttpRequest();
  xhr.open(
    'GET',
    'update.py?modify=yes&idf='+idf+'&key='
      +encodeURIComponent(key.value)+'&quote='
      +encodeURIComponent(phrase.value)+'&keyword='
      +encodeURIComponent(keyword.value)+'&page='
      +encodeURIComponent(page.value)+'&comment='
      +encodeURIComponent(comment.value)
  );
  xhr.onload = function() {{
    if (xhr.status === 200) {{
      loadIDF(node, idf);
        
    }}
    else {{
      alert('Request failed.');
    }}
  }};
  xhr.send();
}}

function showBibTex(node){{
    var falert = document.createElement('div');
    falert.id='fake';
    falert.className='fake_alert';
    var text = '<div class="message"><p>Entry in BibTex</p><p><pre style="overflow-x:scroll;text-align:left;margin:10px;padding:10px;background-color:white;">'+EvoBib[node.dataset.eb]+'</pre></p>';
    text += '<div style="background-color:Crimson;color:white;cursor:pointer;border:2px solid white;" onclick="closeBibTex();">CLOSE</div></div>';
    document.body.appendChild(falert);
    falert.innerHTML=text;
}}
function closeBibTex(){{
  var fake = document.getElementById('fake');
  document.body.removeChild(fake);
}}

function checkloade(event) {{
  if (event.which == 13 || event.keyCode == 13) {{
    loade();
  }}
  else {{
    return;
  }}
}}



if (document.URL.indexOf('?') != -1) {{
  var base, main, keyval, i, what;
  base = document.URL.split('?');
  if (base[1].indexOf('login') != -1) {{
    add();
  }}
  else {{
    main = base[1].split('&');
    for (i=0; i<main.length; i++) {{
      keyval = main[i].split('=');
      if (keyval[0] == 'key' || keyval[0] == 'idf' || keyval[0] == 'keywords'){{
        what = 'tabreiter-0-2';
        document.getElementById('q_'+keyval[0]).value=keyval[1];
      }}
      else {{
        document.getElementById('e_key').value = keyval[1];
        what = 'tabreiter-0-1';
      }}
    }}
    if (what == 'tabreiter-0-1') {{loade()}}
    else {{load();}}
    document.getElementById(what).checked='checked';
  }}
}}



</script>
</body>
</html>
"""

footer = """
<div class="footer"> <div class="footerchild"> <a
href="https://cordis.europa.eu/project/rcn/206320_en.html"><img
src="http://calc.digling.org/img/European_Research_Council_logo.svg" alt="erc-logo"
style="width:100px;"/></a></div> <div class="footerchild"> <p> Last updated on
2019-01-03.</p> 
<p><a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img
alt="Creative Commons License" style="border-width:0"
src="https://i.creativecommons.org/l/by/4.0/88x31.png"></a><br><span
xmlns:dct="http://purl.org/dc/terms/"
href="http://purl.org/dc/dcmitype/InteractiveResource" property="dct:title"
rel="dct:type">This website</span> by <span
xmlns:cc="http://creativecommons.org/ns#"
property="cc:attributionName">Johann-Mattis List</span> is licensed under a <a
rel="license" href="http://creativecommons.org/licenses/by/4.0/"
style="color:white">Creative Commons Attribution 4.0 International License</a>.
</p><p><a style="color:white;"
href="http://www.shh.mpg.de/2417/imprint">IMPRINT</a></p> </div> <div
class="footerchild"> <a href="http://www.shh.mpg.de/375796/calc"> <img
src="http://calc.digling.org/img/max-planck-logo.svg" alt="mpi-logo" style="width:100px;"/></a></div> 
</div> 

"""

print template.format(
        refs=len(keys),
        quotes=sum(keys.values()),
        references=references,
        ac_keys=','.join(sorted(keys)),
        ac_kws=','.join(sorted(keywords, key=lambda x: keywords[x],
            reverse=True)).encode('utf-8'),
        user=user,
        ebdata=','.join(ebdata),
        showcomment='none' if user not in ['Mattis'] else 'inline',
        hidden='display:none' if user not in ['Mattis'] else '',
        footer=footer,
        version=version,
        evoref=','.join([x for x in keys])
        )

