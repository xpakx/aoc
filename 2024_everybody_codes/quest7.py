from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass


@dataclass
class Plan:
    id: str
    actions: list[str]

    def action(self, step: int, num: int) -> int:
        idx = step % len(self.actions)
        act = self.actions[idx]
        if act == '+':
            return num+1
        if act == '-':
            return num-1
        if act == '=':
            return num

    def process(self, init_num: int, steps: int) -> int:
        num = init_num
        result = 0
        print(self.id, end=': ')
        for i in range(steps):
            num = self.action(i, num)
            print(num, end=' ')
            result += num
        print()
        return result


def load(filename):
    data = get_file(filename)
    a = parse(Plan, "{id}:{actions}", data, list_separator=',')
    return a


def task1(data):
    results = [(p.process(10, 10), p) for p in data]
    results.sort(key=lambda p: p[0], reverse=True)
    print(results)
    names = [p.id for _, p in results]
    return "".join(names)


app = AdventDay()
app.run()
