# encoding: utf-8

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
    loadMunicipalityListInDB()
