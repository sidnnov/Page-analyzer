### Hexlet tests and linter status:
[![Actions Status](https://github.com/sidnnov/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/sidnnov/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/54f8ce582e7588530d81/maintainability)](https://codeclimate.com/github/sidnnov/python-project-83/maintainability)

## Page analyzer!
Checking sites for SEO suitability.


#### This application is developed with:
- flask = "^2.2.2"
- gunicorn = "^20.1.0"
- psycopg2-binary = "^2.9.5"
- python-dotenv = "^0.21.1"
- validators = "^0.20.0"
- requests = "^2.28.2"
- beautifulsoup4 = "^4.11.2"
- lxml = "^4.9.2"

#### Installation:
-----------------------

python 3.8+ is required to install page_analyzer. And also need poetry for the assembly of the project.
The project also requires PostgreSQL version 14.5+.

```
$ git clone git@github.com:sidnnov/python-project-83.git
```

Create a .env file and specify your database and secret key there.

```
DATABASE_URL = 'YOUR DATABASE'
SECRET_KEY = 'YOUR SECRETKEY'
```

##### Make commands:
```
install:
	poetry install

start-postgresql:
	sudo service postgresql start

db-create:
	createdb page_analyzer

schema-load:
	psql page_analyzer < database.sql

dev:
	poetry run flask --app page_analyzer:app --debug run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

```

#### Demonstration:
https://test-jlie.onrender.com/
