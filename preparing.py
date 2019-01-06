"""
functions for preparing and loading data
"""

from news import NewsFactory
from collections import Counter


def load(path):
    factory = NewsFactory()
    with open(path) as r:
        lines = r.readlines()
        news = factory.news(lines)
    return news


def count_words_by_tags(news_list):
    counters = {}
    for news in news_list:
        if news.tag not in counters.keys():
            counters[news.tag] = Counter()
        counters[news.tag].update(news.body)

    for tag, counter in counters.items():
        counters[tag] = Counter(
            {word: count for word, count in counter.items() if count > 12}
        )
    return counters


def to_file(filename, list_of_tags):
    with open(filename, "w") as f:
        for tag in list_of_tags:
            f.write(f"{tag}\n")
