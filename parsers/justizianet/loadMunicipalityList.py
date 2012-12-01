# encoding: utf-8

from model import *
from subastas_scrapper import *

def loadMunicipalityListInDB():
    Session = sessionmaker(bind = engine)
    session = Session()

    for municipio in municipios:
        munidb = Municipio(municipio)
        session.add(munidb)
    session.commit()
    session.close()

if __name__ == "__main__":
    print "Creating db schema"
    Base.metadata.create_all(bind = engine)

    print "Loading municiopality list"
    loadMunicipalityListInDB()
