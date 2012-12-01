import urllib2
import os
import getpass
import traceback

os.system("pip install -r requirements.txt")

rhok_db = urllib2.urlopen("http://dev.morelab.deusto.es/rhok_desahucios.sql").read()

open("rhok_desahucios.sql",'w').write(rhok_db)

user = "root"
password = getpass.getpass("Dame password mysql")

import pymysql as dbi
print "Creating database..."
try:
    connection = dbi.connect(user=user, passwd=password, host="127.0.0.1")
    cursor = connection.cursor()
    cursor.execute("""CREATE DATABASE IF NOT EXISTS `rhok_desahucios` ;
    CREATE USER 'rhok'@'localhost' IDENTIFIED BY 'rhok';
    GRANT ALL PRIVILEGES ON `rhok_desahucios`.* TO `rhok`@`localhost`;""")
    connection.commit()
    cursor.close()
    connection.close()
except:
    traceback.print_exc()

print "done"
print "Adding content..."
lines = rhok_db.splitlines()
for line in lines:
    try:
        connection = dbi.connect(user=user, passwd=password, host="127.0.0.1")
        cursor = connection.cursor()
        cursor.execute(line)
        connection.commit()
        cursor.close()
        connection.close()
    except:
        traceback.print_exc()
