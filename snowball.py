"""
add docs later
"""

import re


class Snowball:
    """
    Porter's stemmer for Russian
    """

    _vowel = r"[аеиоуыэюя]"
    _consonant = r"[^аеиоуыэюя]"

    _regexp_rv = re.compile(_vowel)
    _regexp_r1 = re.compile(_vowel + _consonant)

    _regexp_perfective_gerund = re.compile(
        r"(((?P<basis>[ая])(в|вши|вшись))|(ив|ивши|ившись|ыв|ывши|ывшись))$"
    )
    _regexp_adjective = re.compile(
        r"(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$"
    )
    _regexp_participle = re.compile(
        r"(((?P<basis>[ая])(ем|нн|вш|ющ|щ))|(ивш|ывш|ующ))$"
    )
    _regexp_reflexive = re.compile(r"(ся|сь)$")
    _regexp_verb = re.compile(
        r"(((?P<basis>[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно))|(ила|ыла|ена|ейте|уйте|ите|"
        r"или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю))$"
    )
    _regexp_noun = re.compile(
        r"(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$"
    )
    _regexp_superlative = re.compile(r"(ейш|ейше)$")
    _regexp_derivational = re.compile(r"(ост|ость)$")
    _regexp_and = re.compile(r"и$")
    _regexp_nn = re.compile(r"((?<=н)н)$")
    _regexp_soft = re.compile(r"ь$")

    def stemming(self, word):
        """
        Execute the stemming.
        """

        rv_pos, r2_pos = self._find_rv(word), self._find_r2(word)
        word = self._step_1(word, rv_pos)
        word = self._step_2(word, rv_pos)
        word = self._step_3(word, r2_pos)
        word = self._step_4(word, rv_pos)
        return word

    def package_stemming(self, wordlist):
        """
        Execute the stemming for a list of words
        """
        result = []
        for word in wordlist:
            result.append(self.stemming(word))
        return result

    def _find_rv(self, word):
        """
        Search for the RV region.
        """

        rv_match = self._regexp_rv.search(word)
        if not rv_match:
            return len(word)
        return rv_match.end()

    def _find_r2(self, word):
        """
        Search for the R2 region.
        """

        r1_match = self._regexp_r1.search(word)
        if not r1_match:
            return len(word)
        r2_match = self._regexp_r1.search(word, pos=r1_match.end())
        if not r2_match:
            return len(word)
        return r2_match.end()

    def _cut(self, word, ending, pos):
        """
        Cut the specified ending after the specified position.
        """

        match = ending.search(word, pos=pos)
        if match:
            try:
                basis = match.group("basis") or ""
            except IndexError:
                return True, word[: match.start()]
            else:
                return True, word[: match.start() + len(basis)]
        else:
            return False, word

    def _step_1(self, word, rv_pos):
        match, word = self._cut(word, self._regexp_perfective_gerund, rv_pos)
        if match:
            return word
        _, word = self._cut(word, self._regexp_reflexive, rv_pos)
        match, word = self._cut(word, self._regexp_adjective, rv_pos)
        if match:
            _, word = self._cut(word, self._regexp_participle, rv_pos)
            return word
        match, word = self._cut(word, self._regexp_verb, rv_pos)
        if match:
            return word
        _, word = self._cut(word, self._regexp_noun, rv_pos)
        return word

    def _step_2(self, word, rv_pos):
        _, word = self._cut(word, self._regexp_and, rv_pos)
        return word

    def _step_3(self, word, r2_pos):
        _, word = self._cut(word, self._regexp_derivational, r2_pos)
        return word

    def _step_4(self, word, rv_pos):
        _, word = self._cut(word, self._regexp_superlative, rv_pos)
        match, word = self._cut(word, self._regexp_nn, rv_pos)
        if not match:
            _, word = self._cut(word, self._regexp_soft, rv_pos)
        return word
