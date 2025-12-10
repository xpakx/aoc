from utils.loader import get_file
from utils.runner import AdventDay
from dataclasses import dataclass, field
import heapq
import z3


@dataclass
class Pattern:
    pattern: str
    buttons: list[list[int]]
    goal: list[int]

    pattern_mask: int = 0
    goal_mask: int = 0
    buttons_masks: list[int] = field(default_factory=list)

    def __post_init__(self):
        self.goal_mask = self._list_to_mask(self.goal)
        self.buttons_masks = [self._list_to_mask(x) for x in self.buttons]
        self.pattern_mask = self._pattern_to_mask(self.pattern)

    def _list_to_mask(self, lst):
        mask = 0
        for x in lst:
            mask |= 1 << x
        return mask

    def _pattern_to_mask(self, pattern):
        mask = 0
        for i, x in enumerate(pattern):
            if x == '#':
                mask |= 1 << i
        return mask


def load(filename):
    data = get_file(filename, split_lines=True)
    d = []
    for elem in data:
        splitted = elem.split()
        pattern = splitted[0][1:-1]
        goal = splitted[-1][1:-1]
        goal = [int(a) for a in goal.split(',')]
        buttons = [a[1:-1].split(',') for a in splitted[1:-1]]
        for i in range(len(buttons)):
            buttons[i] = [int(a) for a in buttons[i]]
        p = Pattern(pattern=pattern, buttons=buttons, goal=goal)
        d.append(p)

    return d


def print_bin(num):
    print(''.join(reversed(format(num, '#014b')[2:])))


class Node(object):
    def __init__(self, state, step):
        self.val = (state, step)

    def __repr__(self):
        return f'Node value: {self.val}'

    def __lt__(self, other):
        return self.val[1] < other.val[1]


def press(pattern):
    states = [Node(0, 0)]
    heapq.heapify(states)
    visited = set()
    while len(states) > 0:
        state, step = heapq.heappop(states).val
        if state in visited:
            continue
        visited.add(state)

        if state == pattern.pattern_mask:
            return step
        for button in pattern.buttons_masks:
            new_state = state ^ button
            heapq.heappush(states, Node(new_state, step+1))
        # print(step)
        # print_bin(state)
        # print()
    return 0


def task1(data):
    result = 0
    for pattern in data:
        result += press(pattern)
    return result


def solve_pattern(pattern):
    optimizer = z3.Optimize()
    x_vars = [z3.Int(f'x_{i}') for i in range(len(pattern.buttons))]

    for x in x_vars:
        optimizer.add(x >= 0)

    for i, goal_val in enumerate(pattern.goal):
        affects_counter = []
        for j, btn in enumerate(pattern.buttons):
            if i in btn:
                affects_counter.append(x_vars[j])
        optimizer.add(z3.Sum(affects_counter) == goal_val)

    optimizer.minimize(z3.Sum(x_vars))

    if optimizer.check() == z3.sat:
        model = optimizer.model()
        return sum(model[x].as_long() for x in x_vars)
    else:
        raise Exception("Unsolvable pattern")


def task2(data):
    total_presses = 0
    for pattern in data:
        total_presses += solve_pattern(pattern)
    return total_presses


app = AdventDay()
app.run(test=False)
