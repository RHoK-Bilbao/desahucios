Introduction
============

The goal of this project is to be able to correlate the evictions that arising
in Spain with the unemployment, being able to calculate it per region and year.
This idea was defined by `VoxCivica <http://voxcivica.org/>`_ and it is detailed
in `this document
<http://blogs.deusto.es/rhok-bilbao/wp-content/uploads/2012/11/retocivicorhok.pdf>`_.
VoxCivica is a citizen initiative that pursues activating the civil society and
providing tools and knowledge so it can exercise its leading, responsible,
critical and aware role.

The web application is not still running anywhere due to the early state of the
project, but you can download it and run it.

The initial code base was developed during the `RHoK Bilbao
<http://blogs.deusto.es/rhok-bilbao/>`_ in December 2012. RHoK stands for `Random
Hacks of Kindness <http://www.rhok.org>`_, which is a global initiative that
attempts to make the world a better place by developing practical, open source
technology solutions to respond to some of the most complex challenges facing
humanity.

Demo
====

See the app running at http://apps.morelab.deusto.es/voxcivica/

Contributions
=============

Contributions are very welcome. If you're a designer, lawyer, developer,
translator or you find any way to help in this project, you are very welcome to
do it. New issues can be reported `here
<http://github.com/RHoK-Bilbao/desahucios/issues>`_.  Contact us at `TO BE
DEFINED <to be defined>`_.

Developers: feel free to fork the project, do any change and pull request.

How to run it
=============

At this point, the system has three main components, all developed in Python and
using MySQL as the database backend (which should be easily replaced):

* The web application, where the results are shown
* Two crawlers:

  * The SEPE crawler, which retrieves unemployment information about all Spain from SEPE.
  * The Jusitizia.net crawler, which retrieves evictions information from the Basque Country Justice Department.

We're pursuing a `fourth component
<https://github.com/RHoK-Bilbao/desahucios/issues/1>`_ to get information about
eviction in the rest of Spain.

Web application
~~~~~~~~~~~~~~~

The code base is located in the ``desahucios/website`` directory. It is a
`django <http://www.djangoproject.com/>`_ application, so you can refer to the
official documentation on how to run it.

* Install the requirements::

  pip install -r requirements.txt

* Run it (``python manage.py runserver``).

You'll find the client code in the ``templates/website/`` directory, and the
different methods in the ``webapp/views.py`` script.

If you want to get an old dump of the database without generating it, just download it from:

   $ mysql -uroot -p < crawlers/sepe/creation.sql
   $ wget http://www.morelab.deusto.es/pub/desahucios.sql.bz2
   $ wget http://www.morelab.deusto.es/pub/rhok_desahucios.sql.bz2
   $ bzip -d desahucios.sql.bz2
   $ bzip -d rhok_desahucios.sql.bz2
   $ mysql -uroot -p rhok_desahucios < desahucios.sql
   $ mysql -uroot -p rhok_desahucios < rhok_desahucios.sql


SEPE crawler
~~~~~~~~~~~~

The code base is located in the ``desahucios/parsers/sepe`` directory.

* Install the requirements::

  pip install -r requirements.txt

* Create the database (``rhok_desahucios`` and grant privileges to
  ``rhok:rhok``). You can do it by running::

  mysql -uroot -p < creation.sql

* Run ``db_loader.py`` script to retrieve all information and update the database.

*Note:* you can download the latest version of the database from `TOBEDEFINED
<tobedefined>`_.

Justizia.net crawler
~~~~~~~~~~~~~~~~~~~~

The code base is located in the ``desahucios/parsers/justizianet`` directory.

* Create a database ``rhok_desahucios`` (see SEPE crawler).
* Execute ``loadMunicipalityList.py`` to initialize database schema and insert
  municipality list.
* Launch ``subastas_scrapper.py`` to download information from web.

Dependencies: sqlalchemy, django, MySQLdb

*Note:* you can download the latest version of the database from `TOBEDEFINED
<tobedefined>`_.

*Warning:* Execute ``drop_all.py`` to remove database schema and **ALL** data
contained in rhok_desahucios table.

Bugs
====

Please fill them at the `issues page <http://github.com/RHoK-Bilbao/desahucios/issues/>`_.

License
=======

All the code of this project has been released under the `BSD 2-clause license
<http://opensource.org/licenses/BSD-2-Clause>`_. Essentially, you can do
whatever you want with this code (redistribute it, modify it and commercialize
it).

