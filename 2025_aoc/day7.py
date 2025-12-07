from utils.loader import get_map
from utils.runner import AdventDay
from enum import Enum


class Tile(Enum):
    empty = 0
    splitter = 1
    beam = 2


def load(filename):
    return get_map(
            filename, Tile,
            dct={'S': Tile.beam, '^': Tile.splitter}
    )


def print_beam(beam, row):
    for i in range(len(beam)):
        if beam[i]:
            print('|', end='')
        elif row[i] == Tile.splitter:
            print('^', end='')
        else:
            print('.', end='')
    print()


def task1(data):
    beam = [x == Tile.beam for x in data[0]]
    result = 0
    for row in data[1:]:
        for i in range(len(beam)):
            current_beam = beam[i]
            current = row[i]
            if current == Tile.splitter and current_beam:
                result += 1
                beam[i] = False
                beam[i-1] = True
                beam[i+1] = True
        print_beam(beam, row)
    return result


app = AdventDay()
app.run(test=False)
