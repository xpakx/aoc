from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    data = get_file(filename)
    return [prepare_branch(x) for x in data]


def prepare_branch(data):
    data = data.split(',')
    instr = []
    for entry in data:
        dir = entry[0]
        steps = int(entry[1:])
        if dir in ['B', 'D', 'R']:
            steps = -steps
        if dir in ['L', 'R']:
            instr.append((steps, 0, 0))
        if dir in ['D', 'U']:
            instr.append((0, steps, 0))
        if dir in ['F', 'B']:
            instr.append((0, 0, steps))
    return instr


def task1(data):
    height = 0
    max = 0
    for _, y, _ in data[0]:
        height += y
        if height > max:
            max = height
    return max


def add_segments(segments, start, step):
    if step[0] != 0:
        s = step[0]
        r = range(min(0, s), max(0, s)+1)
        print(r, step, start)
        print([(start[0]+x, start[1], start[2]) for x in r])
        segments.update([(start[0]+x, start[1], start[2]) for x in r])
    elif step[1] != 0:
        s = step[1]
        r = range(min(0, s), max(0, s)+1)
        print(r, step, start)
        print([(start[0], start[1]+x, start[2]) for x in r])
        segments.update([(start[0], start[1]+x, start[2]) for x in r])
    else:
        s = step[2]
        r = range(min(0, s), max(0, s)+1)
        print(r, step, start)
        print([(start[0], start[1], start[2]+x) for x in r])
        segments.update([(start[0], start[1], start[2]+x) for x in r])


def task2(data):
    segments = set()
    start = (0, 0, 0)
    for branch in data:
        seg = start
        for x, y, z in branch:
            add_segments(segments, seg, (x, y, z))
            seg = (seg[0]+x, seg[1]+y, seg[2]+z)
    return len(segments)-1


app = AdventDay()
app.run()
