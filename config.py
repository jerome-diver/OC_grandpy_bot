"""Config file"""

from os import environ


class Config(object):
    """All config mode share this global variables"""

    port = int(environ.get('PORT', 5000))

    TESTING = False
    DEBUG = False


class ProductionConfig(Config):
    """Only Production env will override these variables"""

    DEBUG = False


class DevelopmentConfig(Config):
    """Only development env will override these variables"""

    DEBUG = True


class TestingConfig(Config):
    """Only testing env will override these variables"""

    TESTING = True
