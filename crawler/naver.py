import re
import sys
from typing import List

import requests
from bs4 import BeautifulSoup

from crawler.utils import strip_text


class NaverCrawler(object):
    def __init__(self):
        self.session = requests.sessions.Session()

    def crawler(self, keyword: str) -> str:
        blogs: List[str] = []
        posts: List[str] = []
        cafes: List[str] = []

        # Get posts address
        r: requests.Response = self.session.get(url=self.url_formatter(keyword))
        soup = BeautifulSoup(r.text, "lxml")
        r.close()
        for a in soup.find_all("a", href=True):
            print(".", end="")
            sys.stdout.flush()
            href: str = a["href"]
            pat: re.Match = re.match(
                "http(s?)://(?P<format>blog|cafe|post).+/.+/.+", href
            )
            if not pat:
                continue

            if pat.group("format") == "blog":
                blogs.append(href)
            elif pat.group("format") == "post":
                posts.append(href)
            elif pat.group("format") == "cafe":
                cafes.append(href)

        blogs = list(set(blogs))
        posts = list(set(posts))
        # cafes = list(set(cafes))

        body: str = str()
        for blog in blogs:
            print(".", end="")
            sys.stdout.flush()
            r: requests.Response = self.session.get(blog)
            soup = BeautifulSoup(r.text, "lxml")
            r.close()
            r: requests.Response = self.session.get(
                "https://blog.naver.com/" + soup.find("iframe")["src"]
            )
            soup = BeautifulSoup(r.text, "lxml")
            r.close()
            for p in soup.find_all("div", {"class": "se-module se-module-text"}):
                if not p.text:
                    continue
                body += strip_text(p.text) + "\n"

        for post in posts:
            print(".", end="")
            sys.stdout.flush()
            r: requests.Response = self.session.get(post)
            soup = BeautifulSoup(r.text, "lxml")
            r.close()

            body += (
                soup.find("meta", {"property": "nv:news:contents"})["content"] + "\n"
            )

        return body

    @staticmethod
    def url_formatter(keyword: str) -> str:
        return "https://search.naver.com/search.naver?where=view&query={}".format(
            keyword
        )
