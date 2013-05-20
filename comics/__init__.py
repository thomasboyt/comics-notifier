from flask import Flask, request, render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy
import simplejson as json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.sqlite3'
db = SQLAlchemy(app)

from models import Title, Issue, User

@app.route('/search')
def search():
    query = request.args.get('query')
    results = Title.query.filter(Title.title.like(query + r'%')).order_by(Title.title).all()
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

@app.route('/')
def index():
    return render_template('index.html')
