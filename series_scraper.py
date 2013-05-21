import re
from bs4 import BeautifulSoup
import requests

from comics import db
from comics.models import Title

from scraper import scrape_line

if __name__ == "__main__":
    cat_page = requests.get("http://www.comiclist.com/index.php/lists/PlainText/").content
    page = BeautifulSoup(cat_page, 'lxml')
    links = page.find_all('h3', 'bTitle')

    titles = set()

    for link in links:
        page = BeautifulSoup(requests.get(link.a['href']).content, 'lxml')
        content = max(page.find_all('p'), key=len)
        lines = [string for string in content.strings]
        lines = lines[1:]

        for line in lines:
            comic = scrape_line(line)

            if comic['publisher'].isupper() and comic['issue_num']:
                title = comic['title']
                titles.add(title)

    for title in titles:
        existing = Title.query.filter_by(title=title).first()
        if not existing:
            new_title = Title(title)
            db.session.add(new_title)
            db.session.commit()
