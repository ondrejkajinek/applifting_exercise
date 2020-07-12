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
pip install -r requirements.txt
```


Voila, everything is in place and ready to be used.

## Setting up database
Product aggregator uses PostgreSQL backend. Just make sure Postgre is running on localhost. Now it's time to create new user account for our app. Depending on the environment these steps can be a bit different

```
psql -U postgres

>>> CREATE ROLE product_aggregator WITH LOGIN;
>>> CREATE DATABASE product_aggregator WITH OWNER product_aggregator;
```
