from setuptools import setup

setup(
    name='suddendev',
    packages=['suddendev'],
    include_package_data=True,
    install_requires=[
        'flask==0.12',
        'flask_sqlalchemy',
        'flask_socketio',
        'flask_wtf',
        'wtforms',
        'gunicorn==19.7.1',
        'eventlet==0.21.0',
        'psycopg2==2.7.1',
        'celery==4.0.2',
        'redis==2.10.5',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
