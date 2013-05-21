import feedparser
from bs4 import BeautifulSoup
import re
from datetime import datetime

from comics import db
from comics.models import Title, Issue

def scrape_line(line):
    # naive
    line = line.strip('\n')
    items = line.split(',')

    # unwrap quotes around publisher & title
    items[1] = re.match(r'"(.*)"', items[1]).group(1)
    items[2] = re.match(r'"(.*)"', items[2]).group(1)

    RE = r'(.*)\s#(\d+)'
    match = re.match(RE, items[2])

    if match:
        title = match.group(1)
        issue_num = match.group(2)
    else:
        title = items[2]
        issue_num = None

    return {
        "date": datetime.strptime(items[0], "%m/%d/%y"),
        "publisher": items[1],
        "title": title,
        "issue_num": issue_num,
        "price": items[3]
    }
    
def scrape_comics(content):
    soup = BeautifulSoup(content)

    content = max(soup.find_all('p'), key=len)
    lines = [string for string in content.strings]
    lines = lines[1:] # remove CSV header

    comics = []
    title_issue = []

    for line in lines:
        comic = scrape_line(line)

        # "games", "merchandise", etc. are not upper, so this leaves us w/ only comics
        # filtering out no issue num = only single issues, no collections
        if comic['publisher'].isupper() and comic['issue_num']:
            if not (comic['title'], comic['issue_num']) in title_issue:
                comics.append(comic)
                title_issue.append((comic['title'], comic['issue_num']))

    return comics

if __name__ == "__main__":
    feed = feedparser.parse("http://feeds.feedburner.com/ncrl?format=xml")
    newest_timestamp = feed.entries[0].published_parsed
    # if newest_timestamp > last_timestamp
    comics = scrape_comics(feed.entries[0].content[0].value)

    for comic in comics:
        title = Title.query.filter_by(title=comic['title']).first()
        if not title:
            title = Title(comic['title'])
            db.session.add(title)
            db.session.commit()

        existing_issue = Issue.query.filter_by(title=title, number=comic['issue_num']).first()

        if not existing_issue:
            issue = Issue(comic['issue_num'], comic['date'], title)
            db.session.add(issue)
            db.session.commit()
