from kolibri.tools.regexes import Regex
import regex as re


from kolibri.tools.scanner import Scanner
from kolibri.core.entity import Entity
from kolibri.tools import regexes

class CommonRegexExtractor(Scanner):
    """ Simple JavaScript tokenizer using the Scanner class"""

    def __init__(self):
        super(CommonRegexExtractor, self).__init__(regexes)
        self.regexes = regexes

    def process(self, src):

        return self.scan(src)

    def get_matches(self, text):
        return self.process(text)

    def addEntity(self, tok, value, start, end):
        t = Entity(tok, value.strip(), start, end)
        t.idx = self.counter
        self.counter += 1
        self.entities.append(t)

if __name__=='__main__':
    ce=CommonRegexExtractor()
    text=""" 0917-8144415"""
    ents=ce.get_matches(text)

    for e in ents:
        print(e.tojson())