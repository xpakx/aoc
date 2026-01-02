from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename)


def intersection_set(data):
    result = []
    illegal = {'*', '.'}
    for i, row in enumerate(data):
        in_row = set(row)
        curr = []
        for j, cell in enumerate(row):
            in_column = set([x[j] for x in data])
            intersection = in_row.intersection(in_column)
            intersection = intersection.difference(illegal)
            curr.append(intersection)
        result.append(curr)
    return result


def task1(data):
    result = ''
    intersection = intersection_set(data)
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == '.':
                result += intersection[i][j].pop()
    return result


app = AdventDay()
app.run()
