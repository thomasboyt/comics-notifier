from comics import db

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    issues = db.relationship('Issue', backref='title', lazy='select')

    def __init__(self, title):
        self.title = title

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'))

    def __init__(self, number, release_date, issue):
        self.number = number
        self.release_date = release_date
        self.issue = issue
