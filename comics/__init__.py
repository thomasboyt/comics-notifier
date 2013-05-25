from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']
app.config['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_ACCESS_KEY']
app.config['S3_BUCKET_NAME'] = "comics-notifier"
app.config['DEBUG'] = bool(os.getenv('DEBUG', False))
db = SQLAlchemy(app)

if not app.config['DEBUG']:
    s3 = FlaskS3(app)

app.config['MAILGUN_API_KEY'] = os.environ['MAILGUN_API_KEY']
app.config['MAILGUN_DOMAIN'] = os.environ['MAILGUN_DOMAIN']

import views
