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


def make_check_map(data, start):
    check_map = []
    for i, row in enumerate(data):
        check_row = []
        for j, val in enumerate(row):
            check = (start[0] - i)**2 + (start[1] - j)**2
            check_row.append(check)
        check_map.append(check_row)
    return check_map


def sum_for_step(data, check_map, step):
    r2 = step**2
    result = 0
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if check_map[i][j] <= r2:
                result += val
    return result


def part2(data, start):
    check_map = make_check_map(data, start)
    max_r = min(len(data), len(data[0])) // 2
    steps = [sum_for_step(data, check_map, i) for i in range(1, max_r+1)]
    steps = [y-x for x, y in zip([0] + steps, steps)]
    max_val, max_idx = max((val, idx+1) for idx, val in enumerate(steps))
    return max_val*max_idx


app = AdventDay()
app.run()
