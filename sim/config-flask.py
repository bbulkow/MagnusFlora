# this is the configuration file.

# pylint: disable=too-few-public-methods,invalid-name,missing-docstring
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SECRET_KEY = 'this-really-needs-to-be-changed'

# some common variables I've found but don't yet understand
#    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
#    ENABLED_MODULES = ( 'auth', 'users', 'teams', 'api' )

    DEBUG = False
    LOADED_CONFIG_FILE = True

class ProductionConfig(BaseConfig):
	DEBUG = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    TESTING = True
