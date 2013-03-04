from sqlalchemy import Column, Integer, Unicode, Float, DateTime, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relation, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

SQLALCHEMY_ENGINE_STR = 'mysql://rhok:rhok@127.0.0.1/rhok_desahucios'

engine = create_engine(SQLALCHEMY_ENGINE_STR, convert_unicode=True, pool_recycle=3600)

Base = declarative_base()

class Municipio(Base):
	__tablename__ = 'Municipios'
	id = Column(Integer, primary_key = True)
	nombre = Column(Unicode(100))

	def __init__(self, nombre):
		self.nombre = nombre

class PartidoJudicial(Base):
	__tablename__ = 'PartidosJudiciales'
	id = Column(Integer, primary_key = True)
	nombre = Column(Unicode(50))
	organo_judicial = Column(Unicode(200))
	telefono = Column(Unicode(15))
	municipio_id = Column(Integer, ForeignKey('Municipios.id'), nullable = False)
	municipio    = relation(Municipio.__name__, backref = backref('partidosjudiciales', order_by=id, cascade = 'all,delete'))

	def __init__(self, nombre, organo_judicial, telefono, municipio):
		self.nombre = nombre
		self.organo_judicial = organo_judicial
		self.telefono = telefono
		self.municipio = municipio

class Desahucio(Base):
	__tablename__ = 'Desahucios'

	id = Column(Integer, primary_key = True)
	fecha = Column(DateTime)
	url = Column(Unicode(500))
	valoracion = Column(Float)
	cancelado = Column(Boolean)
	deposito = Column(Float)
	resumen = Column(Unicode(200))
	procedimiento_judicial = Column(Unicode(200))
	direccion = Column(Unicode(200))
	nig = Column(Unicode(200))
	municipio_id = Column(Integer, ForeignKey('Municipios.id'), nullable = False)
	municipio    = relation(Municipio.__name__, backref = backref('desahucios', order_by=id, cascade = 'all,delete'))
	partidojudicial_id = Column(Integer, ForeignKey(PartidoJudicial.id), nullable = False)
	partidojudicial    = relation(PartidoJudicial.__name__, backref = backref('partidosjudiciales', order_by=id, cascade = 'all,delete'))
	
	def __init__(self, fecha, url, valoracion, cancelado, deposito, resumen, procedimiento_judicial, direccion, nig, municipio, partidojudicial):
		self.fecha = fecha
		self.url = url
		self.valoracion = valoracion
		self.cancelado = cancelado
		self.deposito = deposito
		self.resumen = resumen
		self.procedimiento_judicial = procedimiento_judicial
		self.direccion = direccion
		self.nig = nig
		self.municipio = municipio
		self.partidojudicial = partidojudicial

