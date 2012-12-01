Solving the following RHoK challenge:

http://blogs.deusto.es/rhok-bilbao/wp-content/uploads/2012/11/retocivicorhok.pdf

# Screen scrapper for www.justizia.net

All scripts are located in *desahucios/parsers/justizianet* folder.

1. Create table *rhok_desahucios*
2. Grant privileges on previous table to *rhok* user with pass *rhok*
3. Execute *loadMunicipalityList.py* to initialize database schema and insert municipality list
4. Launch *subastas_scrapper.py* to download information from web


Warning: Execute *drop_all.py* to remove schema and ALL data contained in rhok_desahucios table. 

# Dependencies

* sqlalchemy
* django
* MySQLdb
