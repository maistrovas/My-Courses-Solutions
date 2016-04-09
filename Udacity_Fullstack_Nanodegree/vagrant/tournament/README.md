Ovarview

- The app is represent a swizz-system tournament DB with some basic functions of it managing, like adding and deleting matches and players, counting themm, and viewing a standing of some tournament.


Database Building

- For creating database i wrote list of commands in 
tournament.sql file as schema.
- CREATE DATABASE name - command that creates database.
- CREATE TABLE name - command for creating tables in database.
- CREATE VIEW name AS query - command for creating a view  that simplifies working wth DB.
- DROP DATABASE if exists - command deletes database vhen we reusing the schema.

Importing DB Schema

- in order to work with the schema in command line I insert '\c DB_name'  command in file that atomatically connect to the DB after typing   '\i DB_name' in pqls.
- python file interact with DB via 'psycopg2' module.

Setup Requirements

- psql
- psycopg2
- python

Test

- Testing available via typing 'python tournament_test.py' that runs test cases from python files.

License

The content of this repository is licensed 
under the [MIT License.](license.md)
