"""
doc
"""

import re
import snowball


class NewsFactory:
    def __init__(self):
        self.stemmer = snowball.Snowball()

        self._regexp_e = re.compile(r"ё")
        self._regexp_clear = re.compile(r"[^A-Za-zА-Яа-я\ ]+")
        self._regexp_space = re.compile(r"\s+")

    def news(self, string_list):
        assert isinstance(string_list, list)

        result = []
        for line in string_list:
            t = line.split("\t")
            body = t.pop()
            t[-1] += " " + body
            t.reverse()
            n = News(*tuple(t))
            n.body = self._regexp_space.sub(
                " ",
                self._regexp_clear.sub(" ", self._regexp_e.sub("е", n.body).lower()),
            ).split(" ")

            n.body = self.stemmer.package_stemming([x for x in n.body if len(x) >= 3])

            # any additional clearing here

            result.append(n)
        return result


class News:
    def __init__(self, body, tag=""):
        self.body = body
        self.tag = tag
