
postgres_restorer
=================

..

   Simple, lightweight tool that manages test databases during integration tests.


   .. image:: https://travis-ci.com/pyux/postgres_restorer.svg?branch=master
      :target: https://travis-ci.com/pyux/postgres_restorer
      :alt: Build Status
    
   .. image:: https://codecov.io/gh/pyux/postgres_restorer/branch/master/graph/badge.svg
      :target: https://codecov.io/gh/pyux/postgres_restorer
      :alt: codecov

    
   .. image:: https://img.shields.io/github/release/pyux/postgres_restorer
      :target: https://GitHub.com/pyux/postgres_restorer/releases/
      :alt: GitHub release


**postgres_restorer** provides fast way of creating/dropping test
 databases and resetting/creating schemas before each test. It also
 wraps **psycopg2** enabling querying created database during tests.
 One instance of PostgresRestorer encapsulates one database,
 if you need to connect to multiple databases, create multiple PostgresRestorer instances, one per tested database.

Installation
------------

.. code-block:: sh

   pip install -U postgres_restorer

Usage
-----


#. 
   Import PostgresRestorer object:

   .. code-block:: python

      from postgres_restorer import PostgresRestorer

#. 
   Create fixture that runs before each test and instantiate PostgresRestorer in it (pytest testing framework used in examples):

   .. code-block:: python

      @pytest.fixture(autouse=True)
      def restorer() -> PostgresRestorer:
       return PostgresRestorer(
           server_connection_string='host=localhost user=test1 password=test1 ',
           test_db_name='test_database',
           dbup_scripts_path='./dbup_scripts',
           test_data_scripts_path='./test_data_scripts'
       )

#. 
   To create database with name specified in 'test_db_name' parameter of PostgresRestorer use:

   .. code-block:: python

      restorer.setup_once()

   If database already exists it will be dropped and recreated.

#. 
   To drop test database after running tests:

   .. code-block:: python

      restorer.teardown_once()

#. 
   To reset/create schema in test database and fill it with test data:

   .. code-block:: python

      restorer.setup()


* **dbup_scripts_path** - location of dbup folder (folder with schema creating sql scripts). Expected folder structure: **dbupscripts/folders/scripts** where folders split scripts into chronologically sortable packages. Names can follow different conventions, for example: **month.year**\ , or **sprint.year**\ , etc. **First dbup script should contain logic resetting all used in database schemas!** Example:
  .. code-block:: sql

     DROP SCHEMA IF EXISTS public;
     CREATE SCHEMA public;


#. 
   To execute no-return query use:

   .. code-block:: python

      restorer.execute(
       query='INSERT INTO test_table(name) VALUES(%(name)s)',
       params={'name': 'test_name'}
      )

   **PostgresRestorer** autocommits queries so there is no need for manual commit.

#. 
   To fetch data from test database:

   .. code-block:: python

      restorer.fetch(
       query='SELECT * FROM test_table WHERE name=%(name)s;',
       params={'name': 'test_name'},
       first=False
      )

   If parameter **first** is set to true only first record from executed query is returned.

Development
-----------

If you wish to expand **postgres_restorer** possibilities, clone repository (master branch).

.. code-block:: sh

   git clone https://github.com/pyux/postgres_restorer.git

Install dependencies:

.. code-block:: sh

   pip install -r requirements.txt

All interface method reside in PostgresRestorer object in *__init.py__* file.

You can run tests for currently developed features by running:

.. code-block:: sh

   pytest test_postgres_restorer.py

Those tests have to be run from inside of *tests* folder since all paths to scripts are declared in relation to it, or you can run **tests_running_script.sh** to achieve same effect.

To run tests running script:

.. code-block:: sh

   sh tests/tests_running_script.sh

To run test coverage:

.. code-block:: sh

   coverage run -m pytest test_postgres_restorer.py

Release History
---------------


* 1.0

  * First version released

License
-------

Distributed under the **MIT License** license. See ``LICENSE`` file for more information.

Github link
===========

`https://github.com/pyux/postgres_restorer <https://github.com/pyux/postgres_restorer>`_

Contributing
------------


#. Fork it (https://github.com/pyux/postgres_restorer/fork)
#. Create your feature branch (\ ``git checkout -b feature/fooBar``\ )
#. Commit your changes (\ ``git commit -am 'Add some fooBar'``\ )
#. Push to the branch (\ ``git push origin feature/fooBar``\ )
#. Create a new Pull Request

**Submits and improvement suggestions are most welcome!**
