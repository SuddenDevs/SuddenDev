#/bin/bash
export DATABASE_URL=postgresql:///suddendev_test
export APP_SETTINGS=suddendev.config.TestingConfig
export SECRET_KEY=test_key_pls_ignore
tox
