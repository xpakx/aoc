from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass


@dataclass
class Note:
    a: int
    b: int
    c: int
    x: int
    y: int
    z: int
    m: int


def load(filename) -> list[Note]:
    return parse(Note, "A={a} B={b} C={c} X={x} Y={y} Z={z} M={m}", get_file(filename))


def eni(n: int, exp: int, mod: int) -> int:
    score = 1
    result = ""
    for _ in range(exp):
        score = (score * n) % mod
        result = str(score) + result
    return int(result)


def eni_for_note(note: Note) -> int:
    result = eni(note.a, note.x, note.m)
    result += eni(note.b, note.y, note.m)
    result += eni(note.c, note.z, note.m)
    return result


def task1(data):
    return max([eni_for_note(x) for x in data])


def eni2(n, exp, mod):
    exps = range(max(exp-4, 0), exp+1)
    out = [pow(n, e, mod) for e in exps]
    return int("".join(map(str, reversed(out))))


def eni_for_note2(note: Note) -> int:
    result = eni2(note.a, note.x, note.m)
    result += eni2(note.b, note.y, note.m)
    result += eni2(note.c, note.z, note.m)
    return result


def task2(data):
    return max([eni_for_note2(x) for x in data])


app = AdventDay()
app.run()
