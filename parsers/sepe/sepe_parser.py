#!/usr/bin/env python
# -*-*- encoding: utf-8 -*-*-

import os
import datetime
import urllib2

# pip install xlrd
import xlrd


class RowRegistry(object):

    def __init__(self, data):

        self.total            = data['total'] or 0

        self.men_less_25      = data['men']['<25'] or 0
        self.men_less_45      = data['men']['25<45'] or 0
        self.men_older        = data['men']['>44'] or 0

        self.women_less_25    = data['women']['<25'] or 0
        self.women_less_45    = data['women']['25<45'] or 0
        self.women_older      = data['women']['>44'] or 0

        self.men              = self.men_less_25   + self.men_less_45   + self.men_older
        self.women            = self.women_less_25 + self.women_less_45 + self.women_older

        self.less_25          = self.men_less_25 + self.women_less_25
        self.less_45          = self.men_less_25 + self.women_less_45
        self.older            = self.men_older   + self.women_older

        self.agriculture      = data['agriculture'] or 0
        self.services         = data['services'] or 0
        self.industry         = data['industry'] or 0
        self.real_estate      = data['real_estate'] or 0
        self.first_employment = data['first_employment'] or 0


class UnemploymentExcelParser(object):
    
    def __init__(self, directory, year, month, province):
        fname = os.path.join(directory, 'xls', str(year), str(month), '%s.xls' % province)

        if not os.path.exists(fname):
            raise Exception("File %s does not exist" % fname)

        print fname

        workbook = xlrd.open_workbook(fname)
        if 'PARO' in workbook.sheet_names():
            sheet_name = 'PARO'
        else:
            potential_sheet_names = [ sheet_name for sheet_name in workbook.sheet_names() if sheet_name.startswith('PARO') ]
            assert len(potential_sheet_names) == 1
            sheet_name = potential_sheet_names[0]

        self.worksheet = workbook.sheet_by_name(sheet_name)
        self.towns     = {}
        self.total     = None

        self.retrieve_data()

    def search_first_town(self):
        # Towns are in col = 1 (second column)

        # TODO: do something smart like "the first row after a space blah blah blah"
        return 8

    def search_last_town(self):
        # Towns are in col = 1 (second column)
        for row in xrange(self.search_first_town(), self.worksheet.nrows):
            town_name = self.worksheet.cell_value(row, 2)
            if town_name == '':
                return row - 1

        return self.worksheet.nrows - 1

    def _format_row(self, row_pos):
        return {
            'total' : self.worksheet.cell_value(row_pos, 2),
            'men' : {
                '<25'   : self.worksheet.cell_value(row_pos, 3),
                '25<45' : self.worksheet.cell_value(row_pos, 4),
                '>44'   : self.worksheet.cell_value(row_pos, 5),
            },
            'women' : {
                '<25'   : self.worksheet.cell_value(row_pos, 6),
                '25<45' : self.worksheet.cell_value(row_pos, 7),
                '>44'   : self.worksheet.cell_value(row_pos, 8),
            },
            'agriculture'      : self.worksheet.cell_value(row_pos, 9),
            'services'         : self.worksheet.cell_value(row_pos, 10),
            'industry'         : self.worksheet.cell_value(row_pos, 11),
            'real_estate'      : self.worksheet.cell_value(row_pos, 12),
            'first_employment' : self.worksheet.cell_value(row_pos, 13),
        }

    def retrieve_data(self):
        initial_row = self.search_first_town()
        last_row    = self.search_last_town()

        print last_row, initial_row
        
        for row_pos in range(initial_row, last_row):
            name = self.worksheet.cell_value(row_pos, 1)
            data = self._format_row(row_pos)
            self.towns[name] = RowRegistry(data)
        
        # Total is after the last town
        total_data = self._format_row(last_row)
        self.total = RowRegistry(total_data)

# Some provices have changed with time. For instance, 
# "Vizcaya" is now "Bizkaia", or "Castellón" is now "Castelló"
PROVINCES = [
   "A_CORUNA", "ARABA", "ALBACETE", "ALICANTE", "ALMERIA", "ASTURIAS", "AVILA",
   "BADAJOZ", "BARCELONA", "BIZKAIA", "BURGOS", "CACERES", "CADIZ", "CANTABRIA",
   "CASTELLON", "CEUTA", "CIUDAD_REAL", "CORDOBA", "CUENCA", "GIRONA",
   "GIPUZKOA", "GRANADA", "GUADALAJARA", "HUELVA", "HUESCA", "BALEARES", "JAEN",
   "LA_RIOJA", "LAS_PALMAS", "LEON", "LLEIDA", "LUGO", "MADRID", "MALAGA",
   "MELILLA", "MURCIA", "NAVARRA", "OURENSE", "PALENCIA", "PONTEVEDRA",
   "SALAMANCA", "TENERIFE", "SEGOVIA", "SEVILLA", "SORIA", "TARRAGONA",
   "TERUEL", "TOLEDO", "VALENCIA", "VALLADOLID", "ZAMORA", "ZARAGOZA",
]

CHANGED_NAMES = {
    'BIZKAIA'   : 'VIZCAYA',
    'ARABA'     : 'ALAVA',
    'GIPUZKOA'  : 'GUIPUZCOA',
}

MONTHS = [
    'Months must be 1..12, and you chose 0',
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
    'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
]

class DownloadException(Exception):
    pass

def iterate_available_data():
    """ returns (year, month, province) for each available data """
    today = datetime.datetime.today()

    for month in range(1, 13):
        for year in range(2005, today.year + 1):
            if year == 2005 and month < 5:
                continue

            if year == today.year and month >= today.month:
                continue

            for province in PROVINCES:
                yield year, month, province

class Downloader(object):
    def __init__(self, directory):
        if not os.path.exists(directory):
            raise Exception("Directory %s does not exist" % directory)

        self.directory = os.path.join(directory, 'xls')

    def _build_url(self, year, month, province):

        month_name = MONTHS[month]

        return 'http://www.sepe.es/contenido/estadisticas/datos_estadisticos/municipios/%(MONTH_COMPLETE)s_%(YEAR_COMPLETE)s/MUNI_%(PROVINCE)s_%(MONTHNUM)s%(YEARNUM)s.xls' % {
            'YEARNUM'  : str(year % 100).zfill(2),
            'MONTHNUM' : str(month).zfill(2),
            'PROVINCE' : province,
            'MONTH_COMPLETE' : month_name,
            'YEAR_COMPLETE'  : year,
        }

    def download(self, year, month, province):
        full_directory = os.path.join(self.directory, str(year), str(month))
        full_path      = os.path.join(full_directory, '%s.xls' % province)

        if os.path.exists(full_path):
            # Already downloaded!
            return

        try:
            url = self._build_url(year, month, province)
            excel_content = urllib2.urlopen(url).read()
        except:
            if province in CHANGED_NAMES:
                url = self._build_url(year, month, CHANGED_NAMES[province])
                try:
                    excel_content = urllib2.urlopen(url).read()
                except:
                    raise DownloadException("Could not download province %s (or %s) for month %s and year %s" % (province, CHANGED_NAMES[province], month, year))
            else:
                raise DownloadException("Could not download province %s for month %s and year %s" % (province, month, year))

        if not os.path.exists(full_directory):
            os.makedirs(full_directory)

        open(full_path, 'w').write(excel_content)

    def download_all(self):
        for year, month, province in iterate_available_data():
            try:
                self.download(year, month, province)
            except DownloadException:
                print "Skipping province %s for month %s and year %s" % (province, month, year)

if __name__ == '__main__':
    
    DIRECTORY = 'stored_data'

    # downloader = Downloader(DIRECTORY)
    # downloader.download_all()

    for year, month, province in iterate_available_data():
    #    continue
        try:
            parser = UnemploymentExcelParser(DIRECTORY, year, month, province)
            parser.retrieve_data()
            print year, month, province, parser.total.total
        except Exception as e:
            print "Error: %s" % e

    # parser = UnemploymentExcelParser(DIRECTORY, 2006, 1, 'ALBACETE')
    # parser.retrieve_data()

