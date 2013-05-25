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

def query_date(date):
    issues = Issue.query.filter_by(release_date=date).all()

    user_cache = defaultdict(lambda : defaultdict(list))

    for issue in issues:
        title = issue.title
        title_id = title.id

        for user in title.users:
            user_cache[user.email][title.title].append(issue)

    return user_cache

def create_mail(users):
    auth = HTTPBasicAuth('api', MAILGUN_API_KEY)
    for user, comics in users.iteritems():
        txt = txt_view.render(comics=comics, user=user)
        html = html_view.render(comics=comics, user=user)
        if not debug:
            r = requests.post(
                url="https://api.mailgun.net/v2/%s/messages" % (MAILGUN_DOMAIN),
                data={
                    "from": "Comics Notifier <notifier@comicsnotifier.mailgun.org>",
                    "to": user,
                    "subject": "New comics releases today",
                    "text": txt,
                    "html": html,
                },
                auth=auth
            )
        else:
            print user
            print txt

if __name__ == "__main__":
    date = datetime(2013, 5, 22)
    create_mail(query_date(date))
