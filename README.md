![sudden-dev logo](logo.png)

[![Build Status](https://travis-ci.org/SuddenDevs/SuddenDev.svg?branch=master)](https://travis-ci.org/SuddenDevs/SuddenDev)

sudden_dev is a proof-of-concept co-op Python scripting game developed in 3 weeks.

Work together as a team to code against waves as enemies.

Getting to the end requires ingenuity and complex team strategies.

You can check it out at [suddendev.io](http://suddendev.io)

It's early days, but we're hoping to take the idea further so give it a go and please send feedback our way at sudddendevcontact@gmail.com

## Running it locally

Requires Python 3 (developed using 3.6) [pip](https://pip.pypa.io/en/stable/installing/), [postgres](https://www.postgresql.org/download/) the [heroku cli](https://devcenter.heroku.com/articles/heroku-cli), and RabbitMQ.

(We're trying to make local development a bit easier...)

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

## Running it on Heroku

We are using Heroku to host the application, and Travis for CI.

The deployment workflow we've set-up is:

- Commit to master
- Travis runs the tests
- If the build is successful, Travis deploys to the staging app of our Heroku pipeline
- One of us may then choose to promote the application to production

If you are looking to try deploying the code to a Heroku app yourself you'll need to:

- Create you're own Heroku App, or multiple on a pipeline
- Add the postgresql add-on to your app(s)
- Add the redis add-on to your heroku app(s)
- Add the CloudAMQP add-on to your heroku app(s)
- Run 'heroku run python clear-db.py' for the app(s) to initialise the database
- Set the APP_SETTINGS envvars on the app, e.g. 'heroku config:set APP_SETTINGS=suddendev.config.ProductionConfig'
- Update the deploy settings in .travis.yml to deploy to your Heroku app and use your own encrypted Heroku API key

Note we have not setup any kind of migration so be careful if changing the DB schema.

Feel free to get in touch at suddendevcontact@gmail.com if you have any questions.
