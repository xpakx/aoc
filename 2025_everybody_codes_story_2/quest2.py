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


def task2(data):
    balloons = data * 100
    balloons = list(balloons)
    balls = 'RGB'
    turn = 0
    while balloons:
        ball_idx = turn % len(balls)
        ball = balls[ball_idx]
        other = None
        if len(balloons) % 2 == 0:
            other = len(balloons) // 2
        if ball == balloons[0] and other is not None:
            balloons.pop(other)
        balloons.pop(0)
        turn += 1
    return turn


app = AdventDay()
app.run()
