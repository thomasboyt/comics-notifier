from datetime import datetime
from collections import defaultdict
import os

from jinja2 import Template, PackageLoader, Environment
import requests
from requests.auth import HTTPBasicAuth

from comics import db
from comics.models import Title, Issue, User

MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
MAILGUN_DOMAIN = os.environ['MAILGUN_DOMAIN']
DEBUG = os.getenv('DEBUG', False)

env = Environment(loader=PackageLoader('comics', 'templates'))
html_view = env.get_template("email/notification.html")
txt_view = env.get_template("email/notification.txt")

auth = HTTPBasicAuth('api', MAILGUN_API_KEY)
def send_mail(user, comics):
    txt = txt_view.render(comics=comics, user=user)
    html = html_view.render(comics=comics, user=user)
    if not DEBUG:
        r = requests.post(
            url="https://api.mailgun.net/v2/%s/messages" % (MAILGUN_DOMAIN),
            data={
                "from": "Comics Notifier <notifier@comicsnotifier.mailgun.org>",
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

    auth = HTTPBasicAuth('api', MAILGUN_API_KEY)
    users = User.query.all()

    for user in users:
        user_issues = new_issues.filter(Title.users.any(user.id == User.id)).all()
        if len(user_issues) > 0:
            issues = [str(issue) for issue in user_issues]
            send_mail(user, issues)

if __name__ == "__main__":
    date = datetime(2013, 5, 22)
    send_mails(date)
