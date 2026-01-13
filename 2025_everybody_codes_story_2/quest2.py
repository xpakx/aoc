from utils.loader import get_file
from utils.runner import AdventDay
from collections import deque


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


class MiddleList:
    def __init__(self, iterable=None):
        self.left = deque()
        self.right = deque()
        if iterable:
            for item in iterable:
                self.append(item)

    def _balance(self):
        if len(self.right) > len(self.left):
            self.left.append(self.right.popleft())
        elif len(self.left) > len(self.right) + 1:
            self.right.appendleft(self.left.pop())

    def append(self, item):
        self.right.append(item)
        self._balance()

    def pop_first(self):
        if not self.left:
            return None

        val = self.left.popleft()
        self._balance()
        return val

    def peek_first(self):
        return self.left[0]

    def pop_middle(self):
        if not self.left:
            return None

        if len(self.left) == len(self.right):
            val = self.right.popleft()
        else:
            val = self.left.pop()

        self._balance()
        return val

    def __len__(self):
        return len(self.left) + len(self.right)

    def __repr__(self):
        return f"[{list(self.left)} | {list(self.right)}]"


def solve_circle(data, repeats):
    balloons = data * repeats
    balloons = MiddleList(balloons)
    balls = 'RGB'
    turn = 0
    while balloons:
        ball_idx = turn % len(balls)
        ball = balls[ball_idx]
        other = False
        if len(balloons) % 2 == 0:
            other = True
        if ball == balloons.peek_first() and other:
            balloons.pop_middle()
        balloons.pop_first()
        turn += 1
    return turn


def task2(data):
    return solve_circle(data, 100)


def task3(data):
    return solve_circle(data, 100000)


app = AdventDay()
app.run()
