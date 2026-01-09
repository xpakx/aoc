from utils.loader import get_file
from utils.runner import AdventDay
from collections import deque


def load(filename):
    data = get_file(filename)
    start = [(i, row.index('S')) for i, row in enumerate(data) if 'S' in row]
    return data, start[0]


dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbors(elem):
    return [(elem[0]+i, elem[1]+j) for i, j in dirs]


def find_path(start, data):
    # alt, steps, pos, prev
    queue = deque([(1000, 0, start, None)])
    visited = {(0, start, None)}
    max_alt = 0
    while queue:
        altitude, steps, curr, prev = queue.popleft()
        if steps == 100:
            if altitude > max_alt:
                max_alt = altitude
            continue
        for neighbor in neighbors(curr):
            if neighbor[0] < 0 or neighbor[1] < 0:
                continue
            if neighbor[0] >= len(data) or neighbor[1] >= len(data[0]):
                continue
            if neighbor == prev:
                continue
            symbol = data[neighbor[0]][neighbor[1]]
            if symbol == '#':
                continue
            new_alt = altitude
            if symbol == '-':
                new_alt -= 2
            elif symbol == '+':
                new_alt += 1
            else:
                new_alt -= 1
            if (new_alt, neighbor, curr) in visited:
                continue
            if new_alt < 0:
                continue
            visited.add((new_alt, neighbor, curr))
            queue.append((new_alt, steps+1, neighbor, curr))
    return max_alt


def part1(data, start):
    return find_path(start, data)


def find_path2(start, data):
    # steps, alt, checkpoints, pos, prev
    queue = deque([(0, 10000, 0, start, None)])
    best_states = {}
    while queue:
        steps, alt, checkpoints, curr, prev = queue.popleft()
        # print(steps, checkpoints, alt, curr, prev)
        if checkpoints == 3 and alt >= 10000 and curr == start:
            return steps

        state_key = (curr, prev, checkpoints)

        if state_key in best_states:
            if best_states[state_key] > alt:
                continue

        for neighbor in neighbors(curr):
            if neighbor[0] < 0:
                continue
            if neighbor == prev:
                continue
            symbol = data[neighbor[0]][neighbor[1]]
            if symbol == '#':
                continue
            new_alt = alt
            if symbol == '-':
                new_alt -= 2
            elif symbol == '+':
                new_alt += 1
            else:
                new_alt -= 1
            c = checkpoints
            if c == 0 and symbol == 'A':
                c = 1
            elif c == 1 and symbol == 'B':
                c = 2
            elif c == 2 and symbol == 'C':
                c = 3

            if new_alt < 9900:
                continue
            if new_alt > 10100:
                continue

            state_key = (neighbor, curr, c)

            if state_key in best_states:
                if best_states[state_key] >= new_alt:
                    continue
            best_states[state_key] = new_alt
            queue.append((steps+1, new_alt, c, neighbor, curr))


def part2(data, start):
    return find_path2(start, data)


def find_path_segment(start, data):
    # alt, steps, pos, prev
    queue = deque([(1000, start, None)])
    max_alt = 0
    dest = start
    best_states = {}
    while queue:
        altitude, curr, prev = queue.popleft()
        if curr[0] == len(data)-1:
            if altitude > max_alt:
                max_alt = altitude
                dest = curr
            continue
        for neighbor in neighbors(curr):
            if neighbor[0] < 0 or neighbor[1] < 0:
                continue
            if neighbor[0] >= len(data) or neighbor[1] >= len(data[0]):
                continue
            if neighbor == prev:
                continue
            symbol = data[neighbor[0]][neighbor[1]]
            if symbol == '#':
                continue
            new_alt = altitude
            if symbol == '-':
                new_alt -= 2
            elif symbol == '+':
                new_alt += 1
            else:
                new_alt -= 1
            if new_alt < 0:
                continue

            state_key = (neighbor, curr)
            if state_key in best_states:
                if best_states[state_key] >= new_alt:
                    continue
            best_states[state_key] = new_alt
            queue.append((new_alt, neighbor, curr))
    return max_alt, dest


def part3(data, start):
    m = {}
    for i in range(len(data[0])-1):
        if i == 0:
            continue
        start = (0, i)
        alt, (_, y) = find_path_segment(start, data)
        m[start] = ((0, y), 1000-alt+1)
    print(m)


app = AdventDay()
app.run()
