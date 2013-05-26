from comics import db

import random
import string

titles_users = db.Table('titles_users',
    db.Column('title_id', db.Integer, db.ForeignKey('title.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    issues = db.relationship('Issue', backref='title', lazy='dynamic')

    def __init__(self, title):
        self.title = title

    def _asdict(self):
        return {
            "id": self.id,
            "title": self.title,
        }

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'))

    def __init__(self, number, release_date, title):
        self.number = number
        self.release_date = release_date
        self.title = title

    def __str__(self):
        return "%s #%s" % (self.title.title, self.number) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    key = db.Column(db.String(24))
    titles = db.relationship('Title', secondary=titles_users, lazy='dynamic', backref='users')

    def __init__(self, email, titles):
        self.email = email
        self.titles = titles

        # generate random key for pseudo-security
        self.key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(24)) 
