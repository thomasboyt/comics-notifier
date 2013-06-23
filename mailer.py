from datetime import datetime
import os

from jinja2 import Template, PackageLoader, Environment
import requests
from requests.auth import HTTPBasicAuth

from comics import app, db
from comics.models import Title, Issue, User

env = Environment(loader=PackageLoader('comics', 'templates'))
html_view = env.get_template("email/notification.html")
txt_view = env.get_template("email/notification.txt")

auth = HTTPBasicAuth('api', app.config['MAILGUN_API_KEY'])
def send_mail(user, comics):
    txt = txt_view.render(comics=comics, user=user)
    html = html_view.render(comics=comics, user=user)
    if not app.config['DEBUG']:
        r = requests.post(
            url="https://api.mailgun.net/v2/%s/messages" % (app.config['MAILGUN_DOMAIN']),
            data={
                "from": "Wham! Pow! Comics Notifier <notifier@comicsnotifier.mailgun.org>",
                "to": user.email,
                "subject": "New comics releases today",
                "text": txt,
                "html": html,
            },
            auth=auth
        )
    else:
        print user.email
        print txt
        print "\n"

def send_mails(date):
    new_issues = db.session.query(Issue).filter(Issue.release_date == date).join(Title)

    auth = HTTPBasicAuth('api', app.config['MAILGUN_API_KEY'])
    users = User.query.all()

    for user in users:
        user_issues = new_issues.filter(Title.users.any(user.id == User.id)).all()
        if len(user_issues) > 0:
            issues = [str(issue) for issue in user_issues]
            send_mail(user, issues)

if __name__ == "__main__":
    date = datetime.today()
    send_mails(date)
