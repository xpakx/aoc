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
    print_msg(msg)
    print()
    dir_i = 0
    for i in range(1, len(msg)-1):
        for j in range(1, len(msg[i])-1):
            dir = instr[dir_i]
            if dir < 0:
                rotate_left(msg, (i, j))
            else:
                rotate_right(msg, (i, j))
            dir_i = (dir_i + 1) % len(instr)
            print_msg(msg)
            print()
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


app = AdventDay()
app.run()
