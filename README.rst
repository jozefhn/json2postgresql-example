Python json2postgresql-example
==============================

Simple script that extracts desired data from json and stores it in postgreSQL database.

Install
-------
Install dependencies:

.. code-block:: bash

    $ poetry install

Supply database credentials: database.ini

Supply example json file: configClear_v2.json

create database table

.. code:: bash

    $ poetry run create-table

Usage
-----

run main script (configClear_v2.json is loaded)

.. code:: bash

    $ poetry run main

run main script (supply path to json file)

.. code:: bash

    $ poetry run main /path/to/json
    
