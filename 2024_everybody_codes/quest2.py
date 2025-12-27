from utils.runner import AdventDay
from pathlib import Path
from itertools import zip_longest


def load(filename):
    data = Path(filename).read_text()
    words, inscriptions = data.split('\n\n')
    words = words.split(':', maxsplit=1)[1].split(',')
    inscriptions = inscriptions.split('\n')
    return words, inscriptions


def task1(words, inscriptions):
    result = 0
    for word in words:
        result += inscriptions[0].count(word)
    return result


app = AdventDay()
app.run()
