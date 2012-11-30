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

municipios = ['ABADIÑO', 'ABANTO Y CIERVANA-ABANTO ZIERBENA', 'AJANGIZ', 'ALONSOTEGI', 'AMOREBIETA-ETXANO', 
'AMOROTO', 'ARAKALDO', 'ARANTZAZU', 'AREATZA', 'ARRANKUDIAGA', 'ARRATZU', 'ARRIETA', 'ARRIGORRIAGA', 'ARTEA', 
'ARTZENTALES', 'ATXONDO', 'AULESTI', 'BAKIO', 'BALMASEDA', 'BARAKALDO', 'BARRIKA', 'BASAURI', 'BEDIA', 'BERANGO', 
'BERMEO', 'BERRIATUA', 'BERRIZ', 'BILBAO', 'BUSTURIA', 'DERIO', 'DIMA', 'DURANGO', 'EA.', 'ELANTXOBE', 'ELORRIO', 
'ERANDIO', 'EREÑO', 'ERMUA', 'ERRIGOITI', 'ETXEBARRI, ANTEIGLESIA DE SAN ESTEBAN-ETXEBARRI DO', 'ETXEBARRIA', 'FORUA', 
'FRUIZ', 'GALDAKAO', 'GALDAMES', 'GAMIZ-FIKA', 'GARAY', 'GATIKA', 'GAUTEGIZ ARTEAGA', 'GERNIKA-LUMO', 'GETXO', 'GIZABURUAGA', 
'GORDEXOLA', 'GORLIZ', 'GÜEÑES', 'IBARRANGELU', 'IGORRE', 'ISPASTER', 'IURRETA', 'IZURTZA', 'KARRANTZA HARANA/VALLE DE CARRANZA', 
'KORTEZUBI', 'LANESTOSA', 'LARRABETZU', 'LAUKIZ', 'LEIOA', 'LEKEITIO', 'LEMOA', 'LEMOIZ', 'LEZAMA', 'LOIU', 'MALLABIA', 
'MARKINA-XEMEIN', 'MARURI-JATABE', 'MAÑARIA', 'MENDATA', 'MENDEXA', 'MEÑAKA', 'MORGA', 'MUNDAKA', 'MUNGIA', 
'MUNITIBAR-ARBATZEGI GERRIKAITZ', 'MURUETA', 'MUSKIZ', 'MUXIKA', 'NABARNIZ', 'ONDARROA', 'OROZKO', 'ORTUELLA', 
'OTXANDIO', 'PLENTZIA', 'PORTUGALETE', 'SANTURTZI', 'SESTAO', 'SONDIKA', 'SOPELANA', 'SOPUERTA', 'SUKARRIETA', 
'TRUCIOS-TURTZIOZ', 'UBIDE', 'UGAO-MIRABALLES', 'URDULIZ', 'URDUÑA-ORDUÑA', 'VALLE DE TRAPAGA-TRAPAGARAN', 'ZALDIBAR', 
'ZALLA', 'ZAMUDIO', 'ZARATAMO', 'ZEANURI', 'ZEBERIO', 'ZIERBENA', 'ZIORTZA-BOLIBAR', 'ALEGRIA-DULANTZI', 'AMURRIO', 'ARAMAIO', 
'ARMIÑON', 'ARRAIA-MAEZTU', 'ARRAZUA-UBARRUNDIA', 'ARTZINIEGA', 'ASPARRENA', 'AYALA/AIARA', 'AÑANA', 'BARRUNDIA', 
'BAÑOS DE EBRO/MAÑUETA', 'BERANTEVILLA', 'BERNEDO', 'CAMPEZO/KANPEZU', 'ELBURGO/BURGELU', 'ELCIEGO', 'ELVILLAR/BILAR', 
'HARANA/VALLE DE ARANA', 'IRURAIZ-GAUNA', 'IRUÑA OKA/IRUÑA DE OCA', 'KRIPAN', 'KUARTANGO', 'LABASTIDA', 'LAGRAN', 'LAGUARDIA', 
'LANCIEGO/LANTZIEGO', 'LANTARON', 'LAPUEBLA DE LABARCA', 'LEGUTIANO', 'LEZA', 'LLODIO', 'MOREDA DE ALAVA', 'NAVARIDAS', 'OKONDO', 
'OYON-OION', 'PEÑACERRADA-URIZAHARRA', 'RIBERA ALTA', 'RIBERA BAJA/ERRIBERA BEITIA', 'SALVATIERRA/AGURAIN', 'SAMANIEGO', 
'SAN MILLAN/DONEMILIAGA', 'URKABUSTAIZ', 'VALDEGOVIA', 'VILLABUENA DE ALAVA/ESKUERNAGA', 'VITORIA-GASTEIZ', 'YECORA/IEKORA', 
'ZALDUONDO', 'ZAMBRANA', 'ZIGOITIA', 'ZUIA', 'ABALTZISKETA', 'ADUNA', 'AIA', 'AIZARNAZABAL', 'ALBIZTUR', 'ALEGIA', 'ALKIZA', 
'ALTZAGA', 'ALTZO', 'AMEZKETA', 'ANDOAIN', 'ANOETA', 'ANTZUOLA', 'ARAMA', 'ARETXABALETA', 'ARRASATE/MONDRAGON', 'ASTEASU', 
'ASTIGARRAGA', 'ATAUN', 'AZKOITIA', 'AZPEITIA', 'BALIARRAIN', 'BEASAIN', 'BEIZAMA', 'BELAUNTZA', 'BERASTEGI', 'BERGARA', 'BERROBI', 
'BIDEGOIAN', 'DEBA', 'DONOSTIA-SAN SEBASTIAN', 'EIBAR', 'ELDUAIN', 'ELGETA', 'ELGOIBAR', 'ERRENTERIA', 'ERREZIL', 'ESKORIATZA', 
'EZKIO-ITSASO', 'GABIRIA', 'GAINTZA', 'GAZTELU', 'GETARIA', 'HERNANI', 'HERNIALDE', 'HONDARRIBIA', 'IBARRA', 'IDIAZABAL', 
'IKAZTEGIETA', 'IRUN', 'IRURA', 'ITSASONDO', 'LARRAUL', 'LASARTE-ORIA', 'LAZKAO', 'LEABURU', 'LEGAZPI', 'LEGORRETA', 
'LEINTZ-GATZAGA', 'LEZO', 'LIZARTZA', 'MENDARO', 'MUTILOA', 'MUTRIKU', 'OIARTZUN', 'OLABERRIA', 'ORDIZIA', 'ORENDAIN', 
'OREXA', 'ORIO', 'ORMAIZTEGI', 'OÑATI', 'PASAIA', 'SEGURA', 'SORALUZE/PLACENCIA DE LAS ARMAS', 'TOLOSA', 'URNIETA', 'URRETXU', 
'USURBIL', 'VILLABONA', 'ZALDIBIA', 'ZARAUTZ', 'ZEGAMA', 'ZERAIN', 'ZESTOA', 'ZIZURKIL', 'ZUMAIA', 'ZUMARRAGA']


municipios = [m.decode("utf-8") for m in municipios]


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
                        #if (evspan.has_key('class') and "location" in evspan['class']):
                        #    location = evspan.contents[0]
                        if (evspan.has_key('class') and "summary" in evspan['class']):
                            detailsurl = evspan.find('a')['href']
                            title = evspan.find('a').contents[0]
                    if isAnyImportantWord(title, importantworddict):
                        scrappEviction(cpartido=cpartido, url=detailsurl, title=title, cancelled=cancelled)

            page += PAGINATION

def scrappEviction(cpartido, url, title, cancelled):
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

    evicdict['URL'] = url
    evicdict['Partido Judicial'] = cpartidos[cpartido]
    evicdict['Resumen'] = title
    evicdict['Cancelado'] = cancelled

    #check valid 'Localidad'
    if not 'Localidad' in evicdict or evicdict['Localidad'] == '.':
        for municipio in municipios:
            if municipio.lower() in title.lower():
                evicdict['Localidad'] = municipio
                break

    if not 'Localidad' in evicdict or not evicdict['Localidad'] in municipios:
	    evicdict['Localidad'] = evicdict['Partido Judicial']

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

