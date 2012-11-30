#!/usr/bin/env python

from sqlalchemy import Column, Integer, Unicode, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relation, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models import SepeProvince, SepeTown, Base
import sepe_parser

class DbLoader(object):

    def __init__(self, directory, username, password, host):
        self.directory = directory
        self.engine_str = 'mysql://%s:%s@%s/rhok_desahucios' % (username, password, host)

    def build_db(self):
        engine = create_engine(self.engine_str, convert_unicode=True, pool_recycle=3600)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def run(self):
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

        for year, month, province in sepe_parser.iterate_available_data():
            try:
                parser = sepe_parser.UnemploymentExcelParser(self.directory, year, month, province)
            except Exception as e:
                print "Error: %s" % e
                continue
                
            registry = provinces[province].create_registry(parser.total, year, month)
            
            session.add(registry)
            
            for town in parser.towns:
                town_instance = session.query(SepeTown).filter_by(province = provinces[province]).first()
                if town_instance is None:
                    town_instance = SepeTown(town, provinces[province])
                    session.add(town_instance)

                registry = town_instance.create_registry(parser.towns[town], year, month)
                session.add(registry)

        session.commit()
        session.close()


if __name__ == '__main__':
    DIRECTORY = 'stored_data'
    loader = DbLoader(DIRECTORY, 'rhok','rhok','127.0.0.1')
    loader.build_db()
    loader.run()

