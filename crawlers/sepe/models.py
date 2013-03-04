from sqlalchemy import Integer, Unicode, Column, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class SepeProvince(Base):

    __tablename__ = 'SepeProvinces'

    id   = Column(Integer, primary_key = True)
    name = Column(Unicode(300), nullable = False)

    def __init__(self, name):
        self.name = name

    def create_registry(self, registry, year, month):
        fields = ('total', 'men', 'women', 'men_less_25', 'women_less_25', 'men_less_45', 'women_less_45', 'men_older', 'women_older', 'less_25', 'less_45', 'older', 'agriculture', 'services', 'industry', 'building', 'first_employment')
        arguments = {
            'province' : self,
            'town'     : None,
            'year'     : year,
            'month'    : month,
        }
        for field in fields:
            arguments[field] = getattr(registry, field)

        return SepeRegistry(**arguments)

class SepeTown(Base):

    __tablename__ = 'SepeTowns'

    id   = Column(Integer, primary_key = True)
    name = Column(Unicode(300), nullable = False)
    
    province_id = Column(Integer, ForeignKey('SepeProvinces.id'), nullable = False)
    province    = relation(SepeProvince.__name__, backref = backref('towns', order_by = id, cascade = 'all,delete'))

    def __init__(self, name, province):
        self.name     = name
        self.province = province

    def create_registry(self, registry, year, month):
        fields = ('total', 'men', 'women', 'men_less_25', 'women_less_25', 'men_less_45', 'women_less_45', 'men_older', 'women_older', 'less_25', 'less_45', 'older', 'agriculture', 'services', 'industry', 'building', 'first_employment')
        arguments = {
            'province' : None,
            'town'     : self,
            'month'    : month,
            'year'     : year,
        }
        for field in fields:
            arguments[field] = getattr(registry, field)

        return SepeRegistry(**arguments)

class SepeRegistry(Base):

    __tablename__ = 'SepeRegistries'

    id          = Column(Integer, primary_key = True)

    total       = Column(Integer, nullable = False)

    year        = Column(Integer, nullable = False)
    month       = Column(Integer, nullable = False)

    men         = Column(Integer, nullable = False)
    women       = Column(Integer, nullable = False)

    men_less_25   = Column(Integer, nullable = False)
    women_less_25 = Column(Integer, nullable = False)

    men_less_45   = Column(Integer, nullable = False)
    women_less_45 = Column(Integer, nullable = False)

    men_older   = Column(Integer, nullable = False)
    women_older = Column(Integer, nullable = False)

    less_25     = Column(Integer, nullable = False)
    less_45     = Column(Integer, nullable = False)
    older       = Column(Integer, nullable = False)

    agriculture      = Column(Integer, nullable = False)
    services         = Column(Integer, nullable = False)
    industry         = Column(Integer, nullable = False)
    building         = Column(Integer, nullable = False)
    first_employment = Column(Integer, nullable = False)


    province_id = Column(Integer, ForeignKey('SepeProvinces.id'))
    province    = relation(SepeProvince.__name__, backref = backref('registries', order_by = id, cascade = 'all,delete'))

    town_id = Column(Integer, ForeignKey('SepeTowns.id'))
    town    = relation(SepeTown.__name__, backref = backref('registries', order_by = id, cascade = 'all,delete'))

    def __init__(self, province, town, year, month, total, men, women, men_less_25, women_less_25, men_less_45, women_less_45, men_older, women_older, less_25, less_45, older, agriculture, services, industry, building, first_employment):

        self.province = province
        self.town     = town

        self.year     = year
        self.month    = month

        self.total    = total
        self.men      = men
        self.women    = women

        self.men_less_25   = men_less_25
        self.women_less_25 = women_less_25
        self.men_less_45   = men_less_45
        self.women_less_45 = women_less_45
        self.men_older     = men_older
        self.women_older   = women_older

        self.less_25       = less_25
        self.less_45       = less_45
        self.older         = older

        self.agriculture      = agriculture
        self.services         = services
        self.industry         = industry
        self.building         = building
        self.first_employment = first_employment

