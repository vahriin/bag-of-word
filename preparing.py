"""
functions for preparing data
"""

from news import NewsFactory


def load(path):
    factory = NewsFactory()
    with open(path) as r:
        lines = r.readlines()
        news = factory.news(lines)
    return news


news = load("news_train.txt")
print(news[:10])

