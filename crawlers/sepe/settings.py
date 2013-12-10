
#SEPE crawler configuration
DIRECTORY = 'stored_data'

START_YEAR = 2005 # Minimum year 2005
END_YEAR = 2013

START_MONTH = 1
END_MONTH = 12

DB_USER = 'rhok'
DB_PASS = 'rhok'
DB_HOST = 'localhost'

DB_STRING = 'mysql://%s:%s@%s/rhok_desahucios' % (DB_USER, DB_PASS, DB_HOST)