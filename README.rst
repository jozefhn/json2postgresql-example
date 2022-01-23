Python json2postgresql-example
==============================

Simple script that extracts desired data from json and stores it in postgreSQL database.

Usage
-----
Install dependecies:
.. code:: bash
    $ poetry install

Supply database credentials: database.ini

Supply example json file: configClear.json

Run scripts:
create database table
.. code:: bash
    $ poetry run create-table

run main script (configClear.json is loaded)
.. code:: bash
    $ poetry run main

run main script (supply path to json file)
.. code:: bash
    $ poetry run main /path/to/json
