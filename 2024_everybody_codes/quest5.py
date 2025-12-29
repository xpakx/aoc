from utils.loader import get_file
from utils.runner import AdventDay
from collections import defaultdict


def load(filename):
    data = get_file(filename)
    data = [[int(item) for item in x.split()] for x in data]
    return [list(col) for col in zip(*data)]


def shouted(data):
    return [col[0] for col in data]


def cycle(data, i):
    row = data[i % len(data)]
    num = row.pop(0)
    next_row = data[(i+1) % len(data)]

    moves = abs((num % (2*len(next_row))) - 1)
    if moves > len(next_row):
        moves = 2*len(next_row) - moves
    next_row.insert(moves, num)


def task1(data):
    # print(data)
    for i in range(10):
        cycle(data, i)
        # print(f"{i+1}:", shouted(data))
    return ''.join(str(x) for x in shouted(data))


def task2(data):
    mem = defaultdict(lambda: 0)
    i = 0
    while True:
        cycle(data, i)
        a, b, c, d = shouted(data)
        num = f"{a}{b}{c}{d}"
        n = mem[num] + 1
        if n == 2024:
            print(num, i)
            return int(num)*(i+1)
        else:
            mem[num] = n
        i += 1


def task3(data):
    max = 0
    i = 0
    visited = set()
    while True:
        cycle(data, i)
        key = tuple(tuple(row) for row in data)
        if key in visited:
            break
        visited.add(key)
        i += 1
        num = int("".join([str(x) for x in shouted(data)]))
        if num > max:
            max = num
    return max


app = AdventDay()
app.run()
