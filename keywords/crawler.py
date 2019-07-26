from bs4 import BeautifulSoup
import requests
from time import sleep
import json
import operator
import functools
import os.path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class KeywordCrawler:
    def __init__(self, subject):
        self.subject = subject
        self.max_depth = 3
        self.url_num = 0
        self.max_url_num = 5000
        self.keywords = {}
        self.filepath = os.path.join(__location__, './data.json')

    def add_keyword(self, keyword):
        if keyword in self.keywords:
            self.keywords[keyword] += 1
        else:
            self.keywords[keyword] = 1

    def parse_keywords(self, query, depth=1):
        if self.url_num > self.max_url_num or depth > self.max_depth:
            return
        else:
            self.url_num += 1
        try:
            html = requests.get(
                'https://ko.wikipedia.org/wiki/{}'.format(query)).text
            soup = BeautifulSoup(html, 'html.parser')
            context = soup.select('.mw-parser-output')[0]
        except BaseException:
            print('[!]', 'Request error')
            return
        if '수학' not in context.text:
            return
        print('[*]', query)
        sleep(0.1)
        paragraphs = context.findAll('p')
        links = [
            p.findAll(
                'a',
                attrs={
                    'class': None},
                recursive=False) for p in paragraphs]
        links = functools.reduce(operator.iconcat, links, [])
        keywords = []
        for link in links:
            href = link.get('href')
            if href and href.startswith('/wiki'):
                keyword = link.text
                self.add_keyword(keyword)
                self.parse_keywords(keyword, depth + 1)
        self.save_keywords_to_file()

    def parse(self):
        self.parse_keywords(self.subject)

    def save_keywords_to_file(self):
        print('[+] Saving keywords to file')
        with open(self.filepath, 'w') as fp:
            json.dump(self.keywords, fp, indent=4, ensure_ascii=False)
            fp.write('\n')

    def load_keywords_from_file(self):
        with open(self.filepath) as fp:
            data = json.load(fp)
        self.keywords = data

    def get_frequent(self, num=100):
        return sorted(
            self.keywords.items(),
            key=operator.itemgetter(1),
            reverse=True)[
            :num]


if __name__ == '__main__':
    crawler = KeywordCrawler('수학')
    crawler.parse()
    print(crawler.get_frequent())
