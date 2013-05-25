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
app.config['DEBUG'] = bool(os.getenv('DEBUG', False))
db = SQLAlchemy(app)
s3 = FlaskS3(app)

MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
MAILGUN_DOMAIN = os.environ['MAILGUN_DOMAIN']
mail_auth = HTTPBasicAuth('api', MAILGUN_API_KEY)

from models import Title, Issue, User

@app.route('/comics')
def comics():
    comics = Title.query.order_by(Title.title).all()
    return json.dumps(comics)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        email = request.args.get('email')
        key = request.args.get('key')
        
        user = User.query.filter_by(email=email).first()
        if not user:
            abort('404')

        return render_template('edit.html', email=user.email, titles=user.titles)

    elif request.method == 'POST':
        email = request.form.get('email')
        key = request.form.get('key')

        user = User.query.filter_by(email=email).first()
        if not user:
            abort('404')

        title_ids = request.form.get('ids').split(',')
        titles = []
        titles = Title.query.filter(Title.id.in_(title_ids)).order_by(Title.title).all()

        user.titles = titles
        db.session.add(user)
        db.session.commit()

        return "{}"

@app.route('/subscribe')
def subscribe():
    email = request.args.get('email')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return json.dumps({
            "error": True,
            "desc": "USER_EXISTS"
        })

    title_ids = request.args.get('ids')
    title_ids = title_ids.split(',')

    titles = []

    titles = Title.query.filter(Title.id.in_(title_ids)).order_by(Title.title).all()
    if len(titles) != len(title_ids):
        return json.dumps({
            "error": True,
            "desc": "TITLE_NOT_FOUND"
        })

    user = User(email, titles)
    db.session.add(user)
    db.session.commit()

    titles = [title.title for title in titles]

    html = render_template("email/confirmation.html", comics=titles)
    txt = render_template("email/confirmation.txt", comics=titles)

    if not app.config['DEBUG']:
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
        return '{}'
    else:
        print txt
        return html

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
    return render_template('index.html')
