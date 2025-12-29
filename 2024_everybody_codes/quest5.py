from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    data = get_file(filename)
    data = [[int(item) for item in x.split()] for x in data]
    return [list(col) for col in zip(*data)]


def shouted(data):
    return [col[0] for col in data]


def task1(data):
    # print(data)
    for i in range(10):
        row = data[i % len(data)]
        num = row.pop(0)
        next_row = data[(i+1) % len(data)]

        moves = num - 1
        if num > len(next_row):
            moves = 2*len(next_row) - moves
        next_row.insert(moves, num)
        # print(f"{i+1}:", shouted(data))

    return ''.join(str(x) for x in shouted(data))


app = AdventDay()
app.run()
