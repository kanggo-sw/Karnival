import os
import sys
from typing import List

from crawler.naver import NaverCrawler


def crawling(keywords: List[str], engines: List[str], output: str) -> None:
    os.makedirs("data/raw")
    for keyword in keywords:
        for engine in engines:
            engine = engine.lower().strip()
            # noinspection PyUnusedLocal
            crawler_instance = None
            if engine == "naver":
                crawler_instance = NaverCrawler()
            else:
                raise NotImplementedError

            print(" - Crawling '{}' on {}".format(keyword, engine), end="")
            sys.stdout.flush()
            with open("data/raw/{}.txt".format(output), "a", encoding="utf8") as data:
                text = crawler_instance.crawler(keyword)
                data.write(text)
