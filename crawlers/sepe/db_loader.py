#!/usr/bin/env python

import os
import datetime

from sqlalchemy import Column, Integer, Unicode, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relation, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models import SepeProvince, SepeTown, Base
import sepe_parser

import settings

today = datetime.datetime.today()

class DbLoader(object):

    def __init__(self):
        self.directory = settings.DIRECTORY
        self.engine_str = settings.DB_STRING

    def build_db(self):
        engine = create_engine(self.engine_str, convert_unicode=True, pool_recycle=3600)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def load_data(self, start_year=2005, end_year=today.year, start_month=1, end_month=12):
        engine = create_engine(self.engine_str, convert_unicode=True, pool_recycle=3600)
        
        Session = sessionmaker(bind = engine)

        session = Session()

        provinces = {}
        
        for province in sepe_parser.PROVINCES:
            province_instance = session.query(SepeProvince).filter_by(name = province).first() 

            if province_instance is None:
                province_instance = SepeProvince(province)
                session.add(province_instance)
            
            provinces[province] = province_instance

        for year, month, province in sepe_parser.iterate_available_data(start_year, end_year, start_month, end_month):
            print 'Processing %s - %s/%s' % (province, month, year)
            try:
                parser = sepe_parser.UnemploymentExcelParser(self.directory, year, month, province)
            except Exception as e:
                print "Error: %s" % e
                continue
                
            registry = provinces[province].create_registry(parser.total, year, month)
            
            session.add(registry)
            
            for town in parser.towns:
                town_instance = session.query(SepeTown).filter_by(province = provinces[province], name = town).first()

                if town_instance is None:
                    town_instance = SepeTown(town, provinces[province])
                    session.add(town_instance)

                registry = town_instance.create_registry(parser.towns[town], year, month)
                session.add(registry)

        session.commit()
        session.close()

    def update(self, start_year=2005, end_year=today.year, start_month=1, end_month=today.month):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        downloader = sepe_parser.Downloader(self.directory)
        downloader.download_all(start_year, end_year, start_month, end_month)

        loader.build_db()
        loader.load_data(start_year, end_year, start_month, end_month)        

if __name__ == '__main__':
    loader = DbLoader()
    loader.update(settings.START_YEAR, settings.END_YEAR, settings.START_MONTH, settings.END_MONTH)

