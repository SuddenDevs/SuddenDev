# SuddenDev

## Development Environment Setup

Requires Python 3.3+ and [pip](https://pip.pypa.io/en/stable/installing/), [postgres](https://www.postgresql.org/download/) and the [heroku cli](https://devcenter.heroku.com/articles/heroku-cli).

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
This can be a pain if you've not already setup postgresql. A helpful guide for ubuntu users can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04).

To initially setup the created development database - and clear it out when developing - run:

```bash
heroku local:run python clear-db.py
```

Finally to run the app locally, simply run:

```bash
heroku local
```

## Testing

We use tox to make sure everything is packed correctly as part of our tests.

Simply install tox (doesn't have to be in the development venv):

```bash
pip install tox
```

And in the root directory, run:

```bash
tox
```

## Deploying to Heroku

TODO
