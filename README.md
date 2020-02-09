![sudden-dev logo](logo.png)

[![Build Status](https://travis-ci.org/SuddenDevs/SuddenDev.svg?branch=master)](https://travis-ci.org/SuddenDevs/SuddenDev)

sudden_dev is a proof-of-concept co-op Python scripting game developed in 3 weeks.

Work together as a team to code against waves as enemies.

Getting to the end requires ingenuity and complex team strategies.

## Running it locally

Requires Python 3 (developed using 3.6) [pip](https://pip.pypa.io/en/stable/installing/), [postgres](https://www.postgresql.org/download/), the [heroku cli](https://devcenter.heroku.com/articles/heroku-cli), and RabbitMQ.

Using a [virtualenv](https://virtualenv.pypa.io/en/stable/)
is recommended. Once virtualenv is installed you can create a virtual environment for Python 3 and activate
it like so:

```bash
virtualenv -p <path to Python 3> venv
source venv/bin/activate
```

Inside the root directory, use pip to install the
suddendev package:

```bash
pip install -e .
```

You will need to install postgresql and create one database for development and another for running tests, named 'suddendev_dev' and 'suddendev_test' respectively.
This can be a pain if you've not already setup postgresql. A helpful guide for Ubuntu users can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04).

In addition, you will need to install rabbitMQ to run it locally.
A helpful guide for this can be found [here](http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html#id4).

To initially setup the created development database - and clear it out when developing - run:

```bash
heroku local:run python clear-db.py
```

Finally to run the app locally as it would be run on Heroku, simply run:

```bash
./run-local-heroku.sh
```

If you want to reset *all* state - the databse and active game data, you can run:

```bash
./clear-all.sh
```

## Testing it Locally

Simply install tox and pytest (neither have to be in the development venv):

```bash
pip install tox pytest
```

And in the root directory, run:

```bash
./run-local-tests.sh
```
