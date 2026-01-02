from utils.loader import get_file
from utils.runner import AdventDay


def load1(filename):
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


def load2(filename):
    data = get_file(filename, split_by='\n\n')
    result = []
    for part in data:
        rows = part.split('\n')
        current = [[x] for x in rows[0].split()]
        for row in rows[1:]:
            for i, elem in enumerate(row.split()):
                current[i].append(elem)

        result.extend(current)
    return result


def task2(data):
    result = 0
    for table in data:
        word = task1(table)
        a = sum([(i+1)*(ord(elem)-64) for i, elem in enumerate(word)])
        result += a
        print(a)
    return result


app = AdventDay()
app.run()
