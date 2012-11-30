# encoding: utf-8

import urllib
import urllib2
import re
import simplejson
import httplib

from BeautifulSoup import BeautifulSoup
from datetime import datetime

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)

DATA_URL = 'http://www.justizia.net/subastas-judiciales'
PAGINATION = 10

startdate = datetime(2012, 05, 01)
enddate = datetime.now()
cpartidos = {
    '0101': 'Amurrio',
    '2002': 'Azpeitia',
    '4805': 'Balmaseda',
    '4802': 'Barakaldo',
    '2003': 'Bergara',
    '4804': 'Bilbao',
    '2005': 'Donostia-San Sebastián',
    '4801': 'Durango',
    '2004': 'Eibar',
    '4803': 'Gernika-Lumo',
    '4806': 'Getxo',
    '2006': 'Irún',
    '2001': 'Tolosa',
    '0102': 'Vitoria-Gasteiz'
}

#wordcounter = {}

importantworddict = [
'vivienda',
#'finca',
#'urbana',
'piso',
'casa',
#'local',
#'parcela',
#'garaje',
#'heredad',
#'lonja',
#'pabellón',
#'solar',
'apartamento',
]

def isAnyImportantWord(phrase, wordlist):
    for w in wordlist:
        if w in phrase.lower():
            return True
    return False

def connection(url):
    print "Connecting to... " + url
    soup = None
    try:
        response = opener.open(url)
        data = response.read()
        soup = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
        #soup = BeautifulSoup(data)
        soup.prettify()
        print "Connection OK"
        return soup
    except:
        print "ERROR! Trying again..."
        connection(url=url)

def scrappList():
    for cpartido in ['0101']: #cpartidos.keys():
        page = 1
        isfinalpage = False
        while not isfinalpage:
            isfinalpage = True            
            params = {
                'cfechaH': enddate.strftime('%d/%m/%Y'),
                'cfechaD': startdate.strftime('%d/%m/%Y'),
                'cpartido': cpartido,
                'ctipo': 'INMU',
                'primerElem': page,
            }

            evlisthtml = connection(DATA_URL + '?' + urllib.urlencode(params))

            for ev in evlisthtml.findAll('tr'):
                if (ev.has_key('class') and "vevent" in ev['class']):
                    cancelled = False
                    if ev.has_key('title'):
                        cancelled = True
                    isfinalpage = False
                    for evspan in ev.findAll('span'):
                        if (evspan.has_key('class') and "location" in evspan['class']):
                            location = evspan.contents[0]
                        elif (evspan.has_key('class') and "summary" in evspan['class']):
                            detailsurl = evspan.find('a')['href']
                            title = evspan.find('a').contents[0]
                    if isAnyImportantWord(title, importantworddict):
                        scrappEviction(cpartido=cpartido, location=location, url=detailsurl, title=title, cancelled=cancelled)
                    
            page += PAGINATION

def scrappEviction(cpartido, location, url, title, cancelled):
    # print cpartidos[cpartido]
    # print location
    # print url
    evicdict = {}

    evhtml = connection(url)
    for det in evhtml.findAll('div'):
        if (det.has_key('class') and "fila" in det['class']):
            for datum in det.findAll('div'):
                if (datum.has_key('class') and "etiqueta" in datum['class']):
                    etiqueta = ''
                    try:
                        etiqueta = datum.contents[0].contents[0]
                    except:
                        etiqueta = datum.contents[0]
                    if etiqueta.encode('utf-8')[-1] == ':':
                        etiqueta = etiqueta.encode('utf-8')[:-1]
                elif (datum.has_key('class') and "dato" in datum['class']):
                    dato = ''
                    try:
                        dato = datum.contents[0].contents[0]
                    except:
                        dato = datum.contents[0]
            evicdict[etiqueta] = dato

    evicdict['Localidad'] = location
    evicdict['URL'] = url
    evicdict['Partido Judicial'] = cpartidos[cpartido]
    evicdict['Resumen'] = title
    evicdict['Cancelado'] = cancelled

    if 'hipotecari' in evicdict['Procedimiento judicial']:
        for a, b in evicdict.items():
            print a
            print b
            print '----'

scrappList()





'''
For wordlist creation:
----------------------

for token in re.split('[.,\/\s]', title):
                        wordcounter[token.lower()] = wordcounter.get(token.lower(), 0) + 1

import operator
sorted_wordlist = sorted(wordcounter.iteritems(), key=operator.itemgetter(1))
for word in sorted_wordlist:
    print word'''