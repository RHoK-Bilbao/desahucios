from sqlalchemy import Column, Integer, Unicode, ForeignKey, UniqueConstraint
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

class User(Base):
	__tablename__ = 'Users'

	id = Column(Integer, primary_key = True)
	username = Column(Unicode(50), nullable = False)
	
	def __init__(self, username):
		self.username = username

class Address(Base):
	__tablename__ = 'Addresses'
	id = Column(Integer, primary_key = True)
	street = Column(Unicode(50), nullable = False)
	user_id = Column(Integer, ForeignKey('Users.id'), nullable = False)
	user = relation(User.__name__, backref = backref('addresses', order_by = id, cascade = 'all,delete'))

	def __init__(self, street, user):
		self.street = street
		self.user   = user


# Base.metadata.drop_all()
Base.metadata.create_all(bind = engine)

Session = sessionmaker(bind = engine)
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
print jon.addresses[0].street

