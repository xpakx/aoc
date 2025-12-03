from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, split_by=",", split_lines=False, as_int=True)


def task1(data):
    nails = max(data)
    step = nails // 2
    result = 0
    for i, j in zip(data, data[1:]):
        if abs(j - i) == step:
            result += 1
    return result


app = AdventDay()
app.run()
