# encoding: utf-8

from model import *
from sqlalchemy import create_engine
from ConfigParser import ConfigParser

if __name__ == "__main__":
    configParser = ConfigParser()
    configParser.read('crawler.cfg')
    db_connection = configParser.get('database', 'db_connection')
    engine = create_engine(db_connection, convert_unicode=True, pool_recycle=3600)

    Base.metadata.drop_all(bind = engine)
