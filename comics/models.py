from comics import db

titles_users = db.Table('titles_users',
    db.Column('title_id', db.Integer, db.ForeignKey('title.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    issues = db.relationship('Issue', backref='title', lazy='select')

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
    release_date = db.Column(db.DateTime)
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'))

    def __init__(self, number, release_date, issue):
        self.number = number
        self.release_date = release_date
        self.issue = issue

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    titles = db.relationship('Title', secondary=titles_users)

    def __init__(self, email, titles):
        self.email = email
        self.titles = titles
