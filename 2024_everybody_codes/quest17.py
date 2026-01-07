from utils.loader import get_file
from utils.runner import AdventDay


def load1(filename):
    data = get_file(filename)
    start = -1
    palms = 0
    for i, row in enumerate(data):
        if row[0] == '.':
            start = i
        for cell in row:
            if cell == 'P':
                palms += 1
    return data, palms, (start, 0)


dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbors(elem):
    return [(elem[0]+i, elem[1]+j) for i, j in dirs]


def flood_fill(start, data, goal):
    filled = set()
    current = start
    steps = 0
    palms = 0
    while current:
        steps += 1
        new_current = []
        for elem in current:
            for neighbor in neighbors(elem):
                if neighbor[0] < 0 or neighbor[1] < 0:
                    continue
                if neighbor[0] >= len(data) or neighbor[1] >= len(data[0]):
                    continue
                symbol = data[neighbor[0]][neighbor[1]]
                if symbol == '#':
                    continue
                if neighbor in filled:
                    continue
                if symbol == 'P':
                    palms += 1
                filled.add(neighbor)
                new_current.append(neighbor)
        if palms == goal:
            return steps
        current = new_current
    return 0


def task1(data, palms, start):
    return flood_fill([start], data, palms)


def load2(filename):
    data = get_file(filename)
    start = -1
    start2 = -1
    palms = 0
    for i, row in enumerate(data):
        if row[0] == '.':
            start = i
        if row[len(row)-1] == '.':
            start2 = i
        for cell in row:
            if cell == 'P':
                palms += 1
    return data, palms, (start, 0), (start2, len(data[0])-1)


def task2(data, palms, start, start2):
    return flood_fill([start, start2], data, palms)


def load3(filename):
    data = get_file(filename)
    palms = 0
    for i, row in enumerate(data):
        for cell in row:
            if cell == 'P':
                palms += 1
    return data, palms


def palm_time(start, data, goal, best):
    filled = set()
    current = [start]
    steps = 0
    palms = 0
    dist = 0
    while current:
        steps += 1
        new_current = []
        for elem in current:
            for neighbor in neighbors(elem):
                symbol = data[neighbor[0]][neighbor[1]]
                if symbol == '#':
                    continue
                if neighbor in filled:
                    continue
                if symbol == 'P':
                    palms += 1
                    dist += steps
                    if dist >= best:
                        return None
                filled.add(neighbor)
                new_current.append(neighbor)
        if palms == goal:
            return dist
        current = new_current
    return None


def task3(data, palms):
    best_time = float('inf')
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == '.':
                time = palm_time((i, j), data, palms, best_time)
                if time and time < best_time:
                    best_time = time
    return best_time


app = AdventDay()
app.run()

