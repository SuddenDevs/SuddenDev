# SuddenDev

## Development Environment Setup

Requires Python 3 (developed using 3.6) [pip](https://pip.pypa.io/en/stable/installing/), [postgres](https://www.postgresql.org/download/) and the [heroku cli](https://devcenter.heroku.com/articles/heroku-cli).

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

## Locally Testing

Simply install tox and pytest (neither have to be in the development venv):

```bash
pip install tox pytest
```

And in the root directory, run:

```bash
tox
```

## Deploying

We are using Heroku to host the application, and Travis for CI.

The deployment workflow we've set-up is:

- Commit to master
- Travis runs the tests
- If the build is successful, Travis deploys to the staging area
- One of us may choose to promote the application in the staging area to production

If you are looking to try deploying the code to a Heroku app yourself you'll need to:

- add the postgresql add-on to your heroku app
- run 'heroku run python clear-db.py' to initialise the database
- set the APP_SETTINGS and SECRET_KEY envvars on the app, e.g. 'heroku config:set APP_SETTINGS=suddendev.config.ProductionConfig'
- update the deploy settings in .travis.yml to deploy to your Heroku app and use your own encrypted Heroku API key
