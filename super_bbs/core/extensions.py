from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_session import Session
from celery import Celery
from flask_redis import FlaskRedis

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
session = Session()
celery = Celery()
redis_store = FlaskRedis()
