# postgres_restorer
> Simple, lightweight tool that manages test databases during integration tests.
>
[![Build Status](https://travis-ci.com/pyux/postgres_restorer.svg?branch=master)](https://travis-ci.com/pyux/postgres_restorer)



**postgres_restorer** provides fast way of creating/dropping test
 databases and resetting/creating schemas before each test. It also
 wraps **psycopg2** enabling querying created databases during tests.

## Installation

```sh
pip install -U postgres_restorer
```

## Usage

1. Import PostgresRestorer object:
 ```python
 from postgres_restorer import PostgresRestorer
 ```

2. Create fixture that runs before each test and instantiate PostgresRestorer in it (pytest testing framework used in examples):
```python
@pytest.fixture(autouse=True)
def restorer() -> PostgresRestorer:
    return PostgresRestorer(
        server_connection_string='host=localhost user=test1 password=test1 ',
        test_db_name='test_database',
        dbup_scripts_path='./dbup_scripts',
        test_data_scripts_path='./test_data_scripts'
    )
```

3. To create database with name specified in 'test_db_name' parameter of PostgresRestorer use:
```python
restorer.setup_once()
```
If database already exists it will be dropped and recreated.

4. To drop test database after running tests:
```python
restorer.teardown_once()
```

5. To reset/create schema in test database and fill it with test data:
```python
restorer.setup()
```
- **dbup_scripts_path** - location of dbup folder (folder with schema creating sql scripts). Expected folder structure: **dbupscripts/folders/scripts** where folders split scripts into chronologically sortable packages. Names can follow different conventions, for example: **month.year**, or **sprint.year**, etc. **First dbup script should contain logic resetting all used in database schemas!** Example:
```sql
DROP SCHEMA IF EXISTS public;
CREATE SCHEMA public;
```

6. To execute no-return query use:
```python
restorer.execute(
    query='INSERT INTO test_table(name) VALUES(%(name)s)',
    params={'name': 'test_name'}
)
```
**PostgresRestorer** autocommits queries so there is no need for manual commit.

7. To fetch data from test database:
```python
restorer.fetch(
    query='SELECT * FROM test_table WHERE name=%(name)s;',
    params={'name': 'test_name'},
    first=False
)
```
If parameter **first** is set to true only first record from executed query is returned.


## Development
If you wish to expand **postgres_restorer** possibilities, clone repository (master branch).
```sh
git clone https://github.com/pyux/postgres_restorer.git
```

Install dependencies:
```sh
pip install -r requirements.txt
```

All interface method reside in PostgresRestorer object in *\_\_init.py\_\_* file.

You can run tests for currently developed features by running:
```sh
pytest test_postgres_restorer.py 
```
Those tests have to be run from inside of *tests* folder since all paths to scripts are declared in relation to it.

To run test coverage:
```sh
coverage run -m pytest test_postgres_restorer.py
```

## Release History

* 1.0
    * First version released


## License
Distributed under the **MIT License** license. See ``LICENSE`` file for more information.

# Github link
[https://github.com/pyux/postgres_restorer](https://github.com/pyux/postgres_restorer)

## Contributing

1. Fork it (<https://github.com/pyux/postgres_restorer/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

**Submits and improvement suggestions are most welcome!**