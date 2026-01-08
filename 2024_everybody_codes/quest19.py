from utils.loader import get_file_instr
from utils.runner import AdventDay


def load(filename):
    instr, msg = get_file_instr(filename, split_second_by='\n')
    instr = [1 if c == 'R' else -1 for c in instr[0]]
    msg = [list(s) for s in msg]
    return instr, msg


def rotate_right(msg, point):
    i, j = point
    temp = msg[i-1][j-1]
    msg[i-1][j-1] = msg[i][j-1]
    msg[i][j-1] = msg[i+1][j-1]
    msg[i+1][j-1] = msg[i+1][j]
    msg[i+1][j] = msg[i+1][j+1]
    msg[i+1][j+1] = msg[i][j+1]
    msg[i][j+1] = msg[i-1][j+1]
    msg[i-1][j+1] = msg[i-1][j]
    msg[i-1][j] = temp


def rotate_left(msg, point):
    i, j = point
    temp = msg[i-1][j-1]
    msg[i-1][j-1] = msg[i-1][j]
    msg[i-1][j] = msg[i-1][j+1]
    msg[i-1][j+1] = msg[i][j+1]
    msg[i][j+1] = msg[i+1][j+1]
    msg[i+1][j+1] = msg[i+1][j]
    msg[i+1][j] = msg[i+1][j-1]
    msg[i+1][j-1] = msg[i][j-1]
    msg[i][j-1] = temp


def print_msg(msg):
    for row in msg:
        for cell in row:
            print(cell, end='')
        print()


def get_msg(msg):
    for row in msg:
        if '>' in row and '<' in row:
            s = row.index('>')
            e = row.index('<')
            return ''.join(row[s+1:e])


def task1(instr, msg):
    dir_i = 0
    for i in range(1, len(msg)-1):
        for j in range(1, len(msg[i])-1):
            dir = instr[dir_i]
            if dir < 0:
                rotate_left(msg, (i, j))
            else:
                rotate_right(msg, (i, j))
            dir_i = (dir_i + 1) % len(instr)
    print(instr)
    print_msg(msg)
    return get_msg(msg)


def task2(instr, msg):
    for _ in range(100):
        dir_i = 0
        for i in range(1, len(msg)-1):
            for j in range(1, len(msg[i])-1):
                dir = instr[dir_i]
                if dir < 0:
                    rotate_left(msg, (i, j))
                else:
                    rotate_right(msg, (i, j))
                dir_i = (dir_i + 1) % len(instr)
    print(instr)
    print_msg(msg)
    return get_msg(msg)


offsets = [(-1, -1), (-1, 0), (-1, 1), (0, 1),
           (1, 1), (1, 0), (1, -1), (0, -1)]


def find_cycles(grid, sequence):
    height, width = len(grid), len(grid[0])
    tgrid = [[(y, x) for x in range(width)] for y in range(height)]
    i = 0
    for y in range(1, height-1):
        for x in range(1, width-1):
            dj = sequence[i % len(sequence)]
            vals = [tgrid[y+dy][x+dx] for (dy, dx) in offsets]
            for j, val in enumerate(vals):
                dy, dx = offsets[(j+dj) % 8]
                tgrid[y+dy][x+dx] = val
            i += 1

    transition = {}
    for y in range(height):
        for x in range(width):
            transition[tgrid[y][x]] = (y, x)

    cycles = []
    seen = set()
    for sy in range(height):
        for sx in range(width):
            if (sy, sx) in seen:
                continue
            cycle = []
            y, x = sy, sx
            while (y, x) not in seen:
                cycle.append((y, x))
                seen.add((y, x))
                y, x = transition[y, x]
            cycles.append(cycle)
    return cycles


def task3(instr, msg):
    rounds = 1048576000
    cycles = find_cycles(msg, instr)

    new_msg = [[None]*len(msg[0]) for _ in range(len(msg))]
    for cycle in cycles:
        for i, (sy, sx) in enumerate(cycle):
            dy, dx = cycle[(i+rounds) % len(cycle)]
            new_msg[dy][dx] = msg[sy][sx]

    return get_msg(new_msg)


app = AdventDay()
app.run()
