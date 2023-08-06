import os


class BaseConfig(object):
    APP_NAME = 'withpano'
    # SERVER_NAME = os.getenv('SERVER_NAME', 'localhost:8023')
    APP_HOST_NAME = os.getenv('APP_HOST_NAME')
    SECRET_KEY = os.getenv('SECRET_KEY', '4aa592fc8883f87ff6d2360983d82529aed2346cfc612f30')
    ENC_PWD = os.getenv('ENC_PWD', 'withpano84265')
    WTF_CSRF_ENABLED = False
    APP_URL_PREFIX = os.getenv('APP_URL_PREFIX', '/')
    URL_SCHEME = os.getenv('URL_SCHEME', 'http')
    STATIC_PATH = os.getenv('STATIC_PATH', 'templates/build')
