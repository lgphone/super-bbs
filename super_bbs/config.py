import os
import redis
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 's8tar0ku120dm3id0s7sd93lr4'
    SESSION_COOKIE_NAME = 'token'
    SESSION_KEY_PREFIX = 'session:'
    REMEMBER_COOKIE_DURATION = timedelta(days=3)
    PERMANENT_SESSION_LIFETIME = timedelta(days=3)

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    SQLALCHEMY_POOL_SIZE = 10
    # SQLALCHEMY_ECHO = True

    LOG_PATH = os.path.join(BASE_DIR, 'logs')
    LOG_PATH_FILE = os.path.join(LOG_PATH, 'run.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024

    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = 'False'

    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, db=0)
    REDIS_URL = 'redis://127.0.0.1:6379/6'

    MAIL_SERVER = 'smtpdm.aliyun.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'noreply@mail.izhihu.me'
    MAIL_DEFAULT_SENDER = 'noreply@mail.izhihu.me'
    # TODO: change password
    MAIL_PASSWORD = ''

    @staticmethod
    def init_app(app):
        pass


class DevConfig(BaseConfig):
    BROKER_URL = 'redis://127.0.0.1:6379/1'
    PRIVATE_KEY_PATH = '/home/yang/.ssh/id_rsa'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask:123456@localhost:3306/super_bbs?charset=utf8mb4'


class TestConfig(BaseConfig):
    BROKER_URL = 'redis://127.0.0.1:6379/1'
    PRIVATE_KEY_PATH = '/home/yang/.ssh/id_rsa'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask:123456@localhost:3306/super_bbs?charset=utf8mb4'


class ProdConfig(BaseConfig):
    DEBUG = False
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, db=0)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask:123456@localhost:3306/super_bbs?charset=utf8mb4'
    BROKER_URL = 'redis://127.0.0.1:6379/1'
    REDIS_URL = 'redis://127.0.0.1:6379/6'
    PRIVATE_KEY_PATH = '/home/yang/.ssh/id_rsa'

    MAIL_SERVER = 'smtpdm.aliyun.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'noreply@mail.izhihu.me'
    MAIL_DEFAULT_SENDER = 'noreply@mail.izhihu.me'
    # TODO: change password
    MAIL_PASSWORD = ''
