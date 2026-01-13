from utils.loader import get_file
from utils.runner import AdventDay


def load(filename) -> tuple[list[str], list[list[int]]]:
    return get_file(filename)[0]


def task1(data):
    pos = 0
    balls = 'RGB'
    turn = 0
    while pos < len(data):
        ball_idx = turn % len(balls)
        while pos < len(data) and data[pos] == balls[ball_idx]:
            pos += 1
        pos += 1
        turn += 1
    return turn



app = AdventDay()
app.run()
