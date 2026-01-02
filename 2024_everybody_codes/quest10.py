from utils.loader import get_file
from utils.runner import AdventDay
from collections import Counter


def load1(filename):
    return get_file(filename)


def intersection_set(data):
    result = []
    illegal = {'*', '.', '?'}
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
    return result


def print_fragment(fragment):
    for row in fragment:
        print(''.join(row))


def get_unique(lst):
    counts = Counter(lst)
    return [item for item, count in counts.items() if count == 1 and item not in ['?', '.', '*']]


def solve_basic(fragment):
    intersection = intersection_set(fragment)
    for i, row in enumerate(fragment):
        for j, cell in enumerate(row):
            s = intersection[i][j]
            if cell == '.' and len(s) == 1:
                fragment[i][j] = s.pop()


def solve_questionmarks(fragment):
    for i, row in enumerate(fragment):
        for j, cell in enumerate(row):
            if cell == '.':
                column = [x[j] for x in fragment]
                unique = []
                col = False
                if '?' in column:
                    unique = get_unique(row)
                    col = True
                elif '?' in row:
                    unique = get_unique(column)
                if len(unique) == 1:
                    fragment[i][j] = unique[0]
                    if col:
                        for x, _ in enumerate(fragment):
                            if fragment[x][j] == '?':
                                fragment[x][j] = unique[0]
                                break
                    else:
                        for x, _ in enumerate(fragment[i]):
                            if fragment[i][x] == '?':
                                fragment[i][x] = unique[0]
                                break


def try_solve_fragment(data, i, j):
    fragment = [row[j:j+8] for row in data[i:i+8]]
    print_fragment(fragment)
    solve_basic(fragment)
    print()
    print_fragment(fragment)
    solve_questionmarks(fragment)
    print()
    print_fragment(fragment)
    for r in range(8):
        data[i + r][j: j + 8] = fragment[r]
    for row in fragment:
        if '.' in row:
            return False
    return True


def load3(filename):
    return [list(x) for x in get_file(filename)]


def get_word(data, i, j):
    result = ''
    for x in range(i+2, i+6):
        for y in range(j+2, j+6):
            result += data[x][y]
    return result


def task3(data):
    run = True
    solved = set()
    while run:
        run = False
        for i in range(0, len(data)-2, 6):
            for j in range(0, len(data[i])-2, 6):
                if (i, j) in solved:
                    continue
                solvable = try_solve_fragment(data, i, j)
                if solvable:
                    solved.add((i, j))
                    run = True

    print_fragment(data)

    result = 0
    for i, j in solved:
        word = get_word(data, i, j)
        power = sum([(i+1)*(ord(elem)-64) for i, elem in enumerate(word)])
        print(word)
        print(power)
        result += power
    return result



app = AdventDay()
app.run()
