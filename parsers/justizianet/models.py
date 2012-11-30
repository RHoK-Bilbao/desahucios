from sqlalchemy import Column, Integer, Unicode, Float, DateTime, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relation, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_ENGINE_STR = 'mysql://rhok:rhok@127.0.0.1/rhok_desahucios'

engine = create_engine(SQLALCHEMY_ENGINE_STR, convert_unicode=True, pool_recycle=3600)

# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))

Base = declarative_base()

class Desahucio(Base):
	__tablename__ = 'Desahucios'

	id = Column(Integer, primary_key = True)
	fecha = Column(DateTime)
	url = Column(Unicode(200))
	valoracion = Column(Float)
	cancelado = Column(Boolean)
	deposito = Column(Float)
	resumen = Column(Unicode(200))
	procedimiento_judicial = Column(Unicode(200))
	direccion = Column(Unicode(200))
	nig = Column(Unicode(200))
	municipio_id = Column(Integer, ForeignKey('Municipios.id'), nullable = False)
	
	def __init__(self, fecha, url, valoracion, cancelado, deposito, resumen, procedimiento_judicial, direccion, nig):
		self.fecha = fecha
		self.url = url
		self.valoracion = valoracion
		self.cancelado = cancelado
		self.deposito = deposito
		self.resumen = resumen
		self.procedimiento_judicial = procedimiento_judicial
		self.direccion = direccion
		self.nig = nig

class PartidoJudicial(Base):
	__tablename__ = 'PartidosJudiciales'
	id = Column(Integer, primary_key = True)
	nombre = Column(Unicode(50))
	organo_judicial = Column(Unicode(200))
	telefono = Column(Unicode(15))
	municipio_id = Column(Integer, ForeignKey('Municipios.id'), nullable = False)

class Municipio(Base):
	__tablename__ = 'Municipios'
	id = Column(Integer, primary_key = True)
	nombre = Column(Unicode(100))

	partidojudicial_id = Column(Integer, ForeignKey('PartidosJudiciales.id'), nullable = True)

	def __init__(self, street, user):
		self.street = street
		self.user   = user

'''class PartidoJudicial(Base):
	__tablename__ = 'PartidosJudiciales'
	id = Column(Integer, primary_key = True)
	nombre = Column(Unicode(50))
	organo_judicial = Column(Unicode(200))
	telefono = Column(Unicode(15))
'''


# Base.metadata.drop_all()
Base.metadata.create_all(bind = engine)

'''Session = sessionmaker(bind = engine)
session = Session()

jon = User(u"jon")
pablo = User(u"pablo")
direccion1 = Address(u"Avenida 1", jon)
direccion2 = Address(u"Avenida 2", jon)

session.add(jon)
session.add(pablo)
session.add(direccion1)
session.add(direccion2)

session.commit()

session.close()

session = Session()
jon = session.query(User).filter_by(username = 'jon').first()
# jon = session.query(User).filter(User.username == 'jon').first()
print jon.addresses
print jon.addresses[0].street'''

