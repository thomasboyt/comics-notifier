from flask import request, render_template, abort

from comics import app, db
from models import Title, User, Issue

import simplejson as json
import requests
from requests.auth import HTTPBasicAuth

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
            abort(404)
        if key != user.key:
            abort(401)

        return render_template('edit.html', email=user.email, titles=user.titles)

    elif request.method == 'POST':
        email = request.form.get('email')
        key = request.form.get('key')

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404)
        if key != user.key:
            abort(401)

        title_ids = request.form.get('ids').split(',')
        titles = []
        titles = Title.query.filter(Title.id.in_(title_ids)).order_by(Title.title).all()

        user.titles = titles
        db.session.add(user)
        db.session.commit()

        return "{}"

mail_auth = HTTPBasicAuth('api', app.config['MAILGUN_API_KEY'])
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

    html = render_template("email/confirmation.html", comics=titles, user=user)
    txt = render_template("email/confirmation.txt", comics=titles, user=user)

    if not app.config['DEBUG']:
        r = requests.post(
            url="https://api.mailgun.net/v2/%s/messages" % (app.config['MAILGUN_DOMAIN']),
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

