from flask import Flask, request, render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3
import simplejson as json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']
app.config['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_ACCESS_KEY']
app.config['MAILGUN_API_KEY'] = os.environ['MAILGUN_API_KEY']
app.config['S3_BUCKET_NAME'] = "comics-notifier"
app.debug = bool(os.getenv('DEBUG', False))
db = SQLAlchemy(app)

s3 = FlaskS3(app)

from models import Title, Issue, User

# verifies mailgun web hooks
import hashlib, hmac
def verify(api_key, token, timestamp, signature):
    return signature == hmac.new(
                             key=api_key,
                             msg='{}{}'.format(timestamp, token),
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

    return "{}"

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    verified = verify(app.config['MAILGUN_API_KEY'], request.args.get('token'), 
                      request.args.get('timestamp'), request.args.get('signature'))

    if verified:
        email = request.args.get('recipient')
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()
    else:
        abort(401)

    return ""

@app.route('/')
def index():
    return render_template('index.html', debug=app.debug)
