from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass
import itertools


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
            if num == 0:
                return 0
            return num-1
        if act == '=':
            return num

    def process(self, init_num: int, steps: int) -> int:
        num = init_num
        result = 0
        for i in range(steps):
            num = self.action(i, num)
            result += num
        return result


def load1(filename):
    data = get_file(filename)
    a = parse(Plan, "{id}:{actions}", data, list_separator=',')
    return a


def task1(data):
    results = [(p.process(10, 10), p) for p in data]
    results.sort(key=lambda p: p[0], reverse=True)
    print([(r, p.id) for r, p in results])
    names = [p.id for _, p in results]
    return "".join(names)


@dataclass
class Track:
    actions: list[str]

    def set_plan(self, plan: Plan):
        self.plan = plan

    def action(self, step: int, num: int) -> int:
        act = self.get_current(step)
        if act == '+':
            return num+1
        if act == '-':
            if num == 0:
                return 0
            return num-1
        return self.plan.action(step-1, num)

    def get_current(self, step: int):
        idx = step % len(self.actions)
        return self.actions[idx]

    def process(self, init_num: int, loops: int = 1) -> int:
        num = init_num
        result = 0
        for i in range(1, loops*len(self.actions) + 1):
            num = self.action(i, num)
            result += num
        assert self.get_current(i) == 'S'
        return result


def load2(filename):
    plans, track = get_file(filename, split_by='\n\n')
    plans = plans.split('\n')
    plans = parse(Plan, "{id}:{actions}", plans, list_separator=',')
    track = track.split('\n')
    top = list(track[0])
    bottom = list(track[-1][::-1])
    center = [x.split() for x in track[1:-1]]
    left = [x[0] for x in center][::-1]
    right = [x[1] for x in center]
    track = Track(top + right + bottom + left)
    return plans, track


def task2(plans, track):
    results = []
    for plan in plans:
        track.set_plan(plan)
        result = track.process(10, 10)
        results.append((result, plan))
    results.sort(key=lambda p: p[0], reverse=True)
    print([(r, p.id) for r, p in results])
    names = [p.id for _, p in results]
    return "".join(names)


dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def construct_path(grid):
    current = (0, 0)
    visited = set()
    visited.add(current)
    path = ['S']
    no_way_further = True
    while no_way_further:
        no_way_further = False
        for dir in dirs:
            x = current[0] + dir[0]
            y = current[1] + dir[1]
            if x < 0 or y < 0:
                continue
            if x >= len(grid) or y >= len(grid[x]):
                continue
            if grid[x][y] == ' ':
                continue
            pos = (x, y)
            if pos in visited:
                continue
            visited.add(pos)
            path.append(grid[x][y])
            current = pos
            no_way_further = True
    return path


def load3(filename):
    plans, track = get_file(filename, split_by='\n\n')
    opponent = parse(Plan, "{id}:{actions}", [plans], list_separator=',')[0]
    track = track.split('\n')
    path = construct_path(track)
    return opponent, Track(path)


def task3(opponent: Plan, track: Track):
    track.set_plan(opponent)
    to_beat = track.process(10, 2024)
    options = set(itertools.permutations('+++++---==='))
    result = 0
    print(len(options))
    for opt in options:
        plan = Plan('A', opt)
        track.set_plan(plan)
        points = track.process(10, 2024)
        if points > to_beat:
            result += 1
    return result


app = AdventDay()
app.run()
