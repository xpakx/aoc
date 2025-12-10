from utils.loader import get_file
from utils.runner import AdventDay
from dataclasses import dataclass, field


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


def press(pattern):
    states = [(0, 0)]
    visited = set()
    while len(states) > 0:
        state, step = states.pop()
        if state in visited:
            continue
        visited.add(state)

        if state == pattern.pattern_mask:
            return step
        for button in pattern.buttons_masks:
            new_state = state ^ button
            states.append((new_state, step+1))
        states.sort(key=lambda x: x[1], reverse=True)
        # print(step)
        # print_bin(state)
        # print()
    return 0


def task1(data):
    print(data)
    result = 0
    for pattern in data:
        result += press(pattern)
    return result


app = AdventDay()
app.run(test=False)
