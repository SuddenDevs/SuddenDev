from setuptools import setup

setup(
    name='suddendev',
    packages=['suddendev'],
    include_package_data=True,
    install_requires=[
        'flask==0.12',
        'flask_sqlalchemy',
        'flask_socketio',
        'gunicorn==19.7.1',
        'eventlet==0.21.0',
        'psycopg2==2.7.1',
        'requests-oauthlib==0.8.0',
        'Flask-Login==0.4.0',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
