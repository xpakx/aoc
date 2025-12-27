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


def find_word(inscription, word, test_set):
    idx = inscription.find(word)
    while idx >= 0:
        for i in range(idx, idx + len(word)):
            test_set.add(i)
        idx = inscription.find(word, idx + 1)


def task2(words, inscriptions):
    result = 0
    words.extend([x[::-1] for x in words])
    test = set()
    for ins in inscriptions:
        for word in words:
            find_word(ins, word, test)
        result += len(test)
        test.clear()
    return result


app = AdventDay()
app.run()
