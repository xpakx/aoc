from utils.loader import get_file_instr
from utils.helpers import transform_steps, clamp, swap
from utils.runner import AdventDay


def load(task: int):
    filename = f"data/everybody_codes_e2025_q01_p{task}.txt"
    [names, instructions] = get_file_instr(filename)
    instructions = transform_steps(instructions)
    return names, instructions


def task1(names, instructions):
    i = 0
    n = len(names)
    for [dir, steps] in instructions:
        i += dir*steps
        i = clamp(i, 0, n-1)
    return names[i]


def task2(names, instructions):
    i = 0
    n = len(names)
    for [dir, steps] in instructions:
        i += dir*steps
        i = i % n
    return names[i]


def task3(names, instructions):
    n = len(names)
    for [dir, steps] in instructions:
        i = dir*steps
        i = i % n
        swap(names, 0, i)
    return names[0]


app = AdventDay()
app.run()
