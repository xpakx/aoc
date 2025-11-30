from pathlib import Path
from dataclasses import dataclass
from utils.parser import parse
from utils.runner import AdventDay


@dataclass
class ComplNumber:
    r: int
    i: int


def mult(a: ComplNumber, b: ComplNumber) -> ComplNumber:
    return ComplNumber(
            r=a.r*b.r - a.i*b.i,
            i=a.r*b.i + a.i*b.r,
    )


def div(a: ComplNumber, b: ComplNumber) -> ComplNumber:
    return ComplNumber(
            r=a.r//b.r if a.r > 0 else -((-a.r)//b.r),
            i=a.i//b.i if a.i > 0 else -((-a.i)//b.i),
    )


def add(a: ComplNumber, b: ComplNumber) -> ComplNumber:
    return ComplNumber(
            r=a.r+b.r,
            i=a.i+b.i,
    )


def load(filename):
    data = Path(filename).read_text(encoding='utf-8')
    return parse(ComplNumber, 'A=[{r},{i}]', data)[0]


def cycle(r, expr, dividor):
    r = mult(r, r)
    r = div(r, ComplNumber(dividor, dividor))
    r = add(r, expr)
    return r


def task1(expr):
    r = ComplNumber(0, 0)

    for c in range(3):
        r = cycle(r, expr, 10)
        print(r)
    return f"[{r.r},{r.i}]"


def check_point(e):
    r = ComplNumber(0, 0)
    for c in range(100):
        r = cycle(r, e, 100000)
        if r.r > 1000000 or r.r < -1000000:
            return False
        if r.i > 1000000 or r.i < -1000000:
            return False
    return True


def task_helper(expr, step, max):
    a = add(expr, ComplNumber(1000, 1000))
    print(a)

    d = ComplNumber(0, 0)
    accepted = 0
    for i in range(max):
        for r in range(max):
            d.r = expr.r + r*step
            d.i = expr.i + i*step
            if check_point(d):
                accepted += 1

    return accepted


def task2(expr):
    return task_helper(expr, 10, 101)


def task3(expr):
    return task_helper(expr, 1, 1001)


app = AdventDay()
app.run()
