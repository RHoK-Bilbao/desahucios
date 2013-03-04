# encoding: utf-8

from model import *
from extra_data import *
from ConfigParser import ConfigParser
from sqlalchemy import create_engine

def loadMunicipalityListInDB():
    Session = sessionmaker(bind = engine)
    session = Session()

    for municipio in municipios:
        munidb = Municipio(municipio)
        session.add(munidb)
    session.commit()
    session.close()

if __name__ == "__main__":
    configParser = ConfigParser()
    configParser.read('crawler.cfg')
    db_connection = configParser.get('database', 'db_connection')
    engine = create_engine(db_connection, convert_unicode=True, pool_recycle=3600)

    print "Creating db schema"
    Base.metadata.create_all(bind = engine)

    print "Loading municiopality list"
    loadMunicipalityListInDB()
