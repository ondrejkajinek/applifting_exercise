[![Travis](https://travis-ci.com/ondrejkajinek/applifting_exercise.svg?branch=master)](https://travis-ci.com/ondrejkajinek/applifting_exercise)
[![codecov](https://codecov.io/gh/ondrejkajinek/applifting_exercise/branch/master/graph/badge.svg)](https://codecov.io/gh/ondrejkajinek/applifting_exercise)

# Applifting exercise

## Requirements
Source code can be cloned from github:

```
git clone https://github.com/ondrejkajinek/applifting_exercise.git
```


Dependencies:

```
python3
```

Other dependencies will be installed into python virtualenv.


## Installation
When source code is downloaded and python installed, we `cd` to project directory and run:

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements_prod.txt
deactivate
```


Voila, everything is in place and ready to be used.

## Setting up database
Product aggregator uses PostgreSQL backend. Just make sure Postgre is running on localhost. Now it's time to create new user account for our app. Depending on the environment these steps can be a bit different

```
psql -U postgres

>>> CREATE ROLE product_aggregator WITH LOGIN;
>>> ALTER USER product_aggregator CREATEDB;
>>> CREATE DATABASE product_aggregator WITH OWNER product_aggregator;
```

## Initialize DB structure
Operation is run from project directory. It has to be run within virtualenv and uses django command for database migrations.

```
. venv/bin/activate
python manage.py migrate
deactivate
```

## Sync application cronjobs to user crontab
Operation is run from project directory. It has to be run within virtualenv and uses django command for cron jobs management

```
. venv/bin/activate
python manage.py crontab add
deactivate
```

## Start the application
Application is served by uwsgi. Configuration is provided in this repository, however, there is a really tiny chance that it will not work. If such thing happens, feel free to report a bug.

If everything is ok, uwsgi should be started with the following command:

```
. venv/bin/activate
uwsgi --yaml conf/product_aggregator.conf
deactivate
```

If you need to restart the service, run the following:

```
. venv/bin/activate
uwsgi --reload run/product_aggregator.pid
deactivate
```

To stop the service, run

```
. venv/bin/activate
uwsgi --stop run/product_aggregator.pid
deactivate
```

# API

The applications exposes several API methods. When calling those, make sure your resource path has trailing slash.

When server error occurs, status code 500 is returned for all methods.

## GET /api/product/
Returns a list of all products. Products without prices are not included.

Status codes:

- 200: OK

Response: list of products, where product looks like

```
{
	"id": integer,
	"name": string,
	"description": string
}
```

## POST /api/product/
Creates new product and register it in Offer microservice.

Request body:

```
{
	"name": string,
	"description": string
}
```
Status codes:

- 201: Created
- 400: Bad request

Response (201): Detail of created product

```
{
	"id": integer,
	"name": string,
	"description": string
}
```

Response (400): Description of error

```
{
	"name": list-of-mistakes, optional,
	"description": list-of-mistakes, optional
}
```

## GET /api/product/{id}/
Retrieves detail for product

Status codes:

- 200: OK
- 404: Not found

Response (200): Product detail

```
	"id": integer,
	"name": string,
	"description": string,
	"offers": list-of-offers
```

Response (404): Not found

```
{
  "detail": "Not found."
}
```

Offer:

```
{
	"id": integer,
	"price": integer,
	"items_in_stock": integer
}
```


## PUT /api/project/{id}/
Updates product. It is not neccessary to send all parameters in request body. Omitted parameters will not be updated by this method.

Request body:

```
{
	"name": string, optional,
	"description": string, optional
}
```

Status codes:

- 200: OK
- 400: Bad request
- 404: Not found

Response (201): Detail of created product

```
{
	"id": integer,
	"name": string,
	"description": string
}
```

Response (400): Description of error

```
{
	"name": list-of-mistakes, optional,
	"description": list-of-mistakes, optional
}
```

Response (404): Not found

```
{
  "detail": "Not found."
}
```


## DELETE /api/project/{id}/
Updates product. It is not neccessary to send all parameters in request body. Omitted parameters will not be updated by this method.

Request body:

```
{
	"name": string, optional,
	"description": string, optional
}
```

Status codes:

- 204: No Content
- 404: Not found

Response (404): Not found

```
{
  "detail": "Not found."
}
```


## GET /api/offer/{id}/changes/
Returns the changes in offer prices throughout the time.

Status codes:

- 200: OK
- 404: Not found

Response (200): List of offer price changes

```
[
	{
		"price": integer,
		"change": float,
		"timestamp_to": integer on null,
		"timestamp_from": integer
	},
	...
]
```

Response (404): Not found

```
{
  "detail": "Not found."
}
```

Only the latest price can have `timestamp_to` equal to `null`. Changes are ordered from the oldest to the current one. The `change` is a relative shift of price with respect to the oldest price (which will always have `change` equal to zero).



# What could also be done
There are tons of things that would follow in the real world. Such as:

- finish tests, e.g., cover more branches, such as several exceptions in a single except statement, check if all transactions are truly transactional
- optimize db queries, prepare tests that ensure only the minimal amount of queries is being run (make sure no n + 1 queries can happen)
- optimize data serialization, e.g., use read-only serializers when possible, or even replace when simple db data are being returned
- use redis for some extra performance
- query only required columns
- pagination for GET methods
