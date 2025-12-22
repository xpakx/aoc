from utils.runner import AdventDay
from utils.loader import get_file


def load(filename):
    data = get_file(filename)
    start = (0, 0)
    for i, row in enumerate(data):
        data[i] = [int(x) if x != '@' else 0 for x in row]
        if '@' in row:
            j = row.index('@')
            start = (i, j)
    return data, start


def check(start, point, r2):
    check = (start[0] - point[0])**2 + (start[1] - point[1])**2
    return check <= r2


def part1(data, start):
    r = 10
    r2 = r**2
    result = 0
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if check(start, (i, j), r2):
                result += val
    return result


app = AdventDay()
app.run()
