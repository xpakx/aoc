from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    data = get_file(filename, split_by=',')
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
    for _, y, _ in data:
        height += y
        if height > max:
            max = height
    return max


app = AdventDay()
app.run()
