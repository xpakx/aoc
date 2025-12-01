from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    data = get_file(filename, split_lines=False)
    return data


def task1(data):
    result = 0
    mentors = 0
    for c in data:
        if c == 'A':
            mentors += 1
        elif c == 'a':
            result += mentors
    return result


app = AdventDay()
app.run()
