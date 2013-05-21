from flask import Flask, request, render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3

import simplejson as json
import requests
from requests.auth import HTTPBasicAuth
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']
app.config['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_ACCESS_KEY']
app.config['S3_BUCKET_NAME'] = "comics-notifier"
app.debug = bool(os.getenv('DEBUG', False))
db = SQLAlchemy(app)

s3 = FlaskS3(app)

from models import Title, Issue, User

MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
MAILGUN_DOMAIN = os.environ['MAILGUN_DOMAIN']
mail_auth = HTTPBasicAuth('api', MAILGUN_API_KEY)

# verifies mailgun web hooks
import hashlib, hmac
def verify(api_key, token, timestamp, signature):
    return signature == hmac.new(
                             key=api_key,
                             msg='{0}{1}'.format(timestamp, token),
                             digestmod=hashlib.sha256).hexdigest()

@app.route('/search')
def search():
    query = request.args.get('query')
    results = Title.query.filter(Title.title.ilike(query + r'%')).order_by(Title.title).all()
    return json.dumps(results)

@app.route('/title/<title>')
def title(title):
    result = Title.query.filter_by(title=title).first()
    if not result:
        abort(404)
    else:
        return json.dumps(result)

@app.route('/subscribe')
def subscribe():
    # TODO: Check for pre-existing user

    email = request.args.get('email')
    title_ids = request.args.get('ids')
    title_ids = title_ids.split(',')

    titles = []

    for id in title_ids:
        title = Title.query.filter_by(id=id).first()
        if not title:
            return json.dumps({
                "error": True,
                "desc": "TITLE_NOT_FOUND"
            })
        titles.append(title)

    user = User(email, titles)
    db.session.add(user)
    db.session.commit()

    titles = [title.title for title in titles]

    html = render_template("confirmation.html", comics=titles)
    txt = render_template("confirmation.txt", comics=titles)

    r = requests.post(
        url="https://api.mailgun.net/v2/%s/messages" % (MAILGUN_DOMAIN),
        data={
            "from": "Comics Notifier <notifier@comicsnotifier.mailgun.org>",
            "to": user.email,
            "subject": "Subscription confirmation",
            "text": txt,
            "html": html,
        },
        auth=mail_auth
    )

    return "{}"

@app.route('/unsubscribe')
def unsubscribe():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        db.session.delete(user)
        db.session.commit()

    return render_template("unsubscribe.html")

@app.route('/')
def index():
    return render_template('index.html', debug=app.debug)
