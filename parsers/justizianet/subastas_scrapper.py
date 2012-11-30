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

municipios = [
    'San Millán', 'Valdegovía', 'Kuartango', 'Labastida',
    'Valle de Arana', 'Laguardia', 'Oyón-Oion', 'Baños de Ebro/Mañueta',
    'Elburgo', 'Añana', 'Legutiano', 'Zigoitia', 'Aramaio',
    'Arrazua-Ubarrundia', 'Llodio', 'Peñacerrada-Urizaharra',
    'Asparrena', 'Bernedo', 'Kripan', 'Moreda de Álava', 'Samaniego',
    'Leza', 'Arraia-Maeztu', 'Elciego', 'Elvillar', 'Armiñón', 'Lantarón',
    'Vitoria-Gasteiz', 'Villabuena de Álava', 'Ribera Baja',
    'Iruña de Oca', 'Zalduondo', 'Ribera Alta', 'Zambrana', 'Zuia',
    'Navaridas', 'Artziniega', 'Barrundia', 'Lanciego', 'Okondo',
    'Yécora', 'Amurrio', 'Berantevilla', 'Iruraiz-Gauna', 'Salvatierra',
    'Lapuebla de Labarca', 'Campezo', 'Lagrán', 'Urkabustaiz', 'Ayala',
    'Alegría-Dulantzi', 'Basauri', 'Aulesti', 'Arrankudiaga', 'Sopelana',
    'Nabarniz', 'Artea', 'Orduña', 'Zaldibar', 'Muskiz', 'Ondarroa',
    'Abanto y Ciérvana', 'Artzentales', 'Maruri-Jatabe', 'Meñaka',
    'Ispaster', 'Dima', 'Ubide', 'Atxondo', 'Markina-Xemein', 'Ortuella',
    'Kortezubi', 'Santurtzi', 'Sopuerta', 'Portugalete', 'Ereño',
    'Arratzu', 'Ermua', 'Abadiño', 'Balmaseda', 'Arakaldo', 'Larrabetzu',
    'Bakio', 'Zierbena', 'Zaratamo', 'Erandio', 'Ugao-Miraballes',
    'Amorebieta-Etxano', 'Bedia', 'Ibarrangelu', 'Iurreta', 'Sukarrieta',
    'Mallabia', 'Ziortza-Bolibar', 'Mañaria', 'Etxebarria', 'Sestao',
    'Mendata', 'Derio', 'Urduliz', 'Galdames', 'Galdakao', 'Lekeitio',
    'Elorrio', 'Murueta', 'Muxika', 'Otxandio', 'Igorre', 'Mundaka',
    'Laukiz', 'Morga', 'Arrigorriaga', 'Elantxobe', 'Carranza', 'Mendexa',
    'Getxo', 'Ajangiz', 'Lemoiz', 'Zeanuri', 'Orozko', 'Loiu', 'Mungia',
    'Sondika', 'Gamiz-Fika', 'Barrika', 'Garai', 'Zamudio', 'Amoroto',
    'Berriatua', 'Lezama', 'Durango', 'Ea', 'Arantzazu', 'Errigoiti',
    'Leioa', 'Trápaga', 'Trucios-Turtzioz', 'Izurtza', 'Arrieta',
    'Etxebarri', 'Bilbao', 'Gizaburuaga', 'Munitibar', 'Gordexola',
    'Zeberio', 'Alonsotegi', 'Fruiz', 'Plentzia', 'Gorliz', 'Gernika-Lumo',
    'Busturia', 'Bermeo', 'Gautegiz Arteaga', 'Güeñes', 'Lanestosa',
    'Areatza', 'Lemoa', 'Zalla', 'Forua', 'Berango', 'Gatika', 'Berriz',
    'Barakaldo', 'Ormaiztegi', 'Altzo', 'Orendain', 'Idiazabal', 'Gaintza',
    'Zumarraga', 'Segura', 'Gabiria', 'Lezo', 'Zestoa', 'Mutiloa',
    'Astigarraga', 'Zegama', 'Aizarnazabal', 'Orio', 'Elgeta', 'Irun',
    'Zaldibia', 'Orexa', 'Lazkao', 'Tolosa', 'Belauntza', 'Mendaro',
    'Olaberria', 'Ezkio-Itsaso', 'Alegia', 'Azpeitia', 'Leintz-Gatzaga',
    'Urretxu', 'Berrobi', 'Zumaia', 'Albiztur', 'Aia', 'Anoeta',
    'Larraul', 'Amezketa', 'Usurbil', 'Deba', 'Getaria', 'Baliarrain',
    'Alkiza', 'Arama', 'Asteasu', 'Lizartza', 'Oñati', 'Villabona',
    'Lasarte-Oria', 'Berastegi', 'Eskoriatza', 'Ikaztegieta',
    'Abaltzisketa', 'Ordizia', 'Aduna', 'Errezil', 'Hondarribia',
    'Aretxabaleta', 'Legorreta', 'Elduain', 'Leaburu', 'Bergara',
    'Andoain', 'Ibarra', 'Mutriku', 'Zizurkil', 'Bidegoian', 'Irura',
    'Altzaga', 'Gaztelu', 'Zarautz', 'Hernialde', 'Errenteria',
    'Oiartzun', 'Urnieta', 'Soraluze-Placencia de las Armas', 'Ataun',
    'Beizama', 'Azkoitia', 'Pasaia', 'Elgoibar', 'Itsasondo', 'Hernani',
    'Eibar', 'Arrasate-Mondragón', 'Donostia-San Sebastián', 'Zerain',
    'Beasain', 'Legazpi', 'Antzuola']

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

    for municipio in municipios:
        if municipio.lower() in title.lower():
            evicdict['Municipio'] = municipio
            break

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

