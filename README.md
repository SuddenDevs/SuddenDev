# SuddenDev

## Local Installation & Usage

Requires Python 3.3+ and [pip](https://pip.pypa.io/en/stable/installing/).

Using a [virtualenv](https://virtualenv.pypa.io/en/stable/)
is recommended. Once installed you can create a virtual environment for Python 3 and activate
it like so:

```bash
virtualenv -p <path to Python 3> venv
source venv/bin/activate
```

Inside the root directory, then use pip to install the
suddendev package:

```bash
pip install -e .
```

To setup the database for the app (or clear it), run:

```bash
python debug-create-new-db.py
```

Finally to run the app:

```bash
python debug.py
```

And to run tests:

```bash
python setup.py test
```
