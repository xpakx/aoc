from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass
from collections import Counter


@dataclass
class Sequence:
    id: int
    seq: str
    a_mask: int = 0
    t_mask: int = 0
    c_mask: int = 0
    g_mask: int = 0

    def init(self):
        for i in range(len(self.seq)):
            self.a_mask <<= 1
            self.t_mask <<= 1
            self.c_mask <<= 1
            self.g_mask <<= 1
            if self.seq[i] == 'A':
                self.a_mask += 1
            elif self.seq[i] == 'T':
                self.t_mask += 1
            elif self.seq[i] == 'C':
                self.c_mask += 1
            elif self.seq[i] == 'G':
                self.g_mask += 1

    def common(self, other):
        a = self.a_mask & other.a_mask
        t = self.t_mask & other.t_mask
        c = self.c_mask & other.c_mask
        g = self.g_mask & other.g_mask
        return (a | t | c | g).bit_count()

    def parents(self, parent1, parent2):
        a = self.a_mask & ~(parent1.a_mask | parent2.a_mask)
        t = self.t_mask & ~(parent1.t_mask | parent2.t_mask)
        c = self.c_mask & ~(parent1.c_mask | parent2.c_mask)
        g = self.g_mask & ~(parent1.g_mask | parent2.g_mask)
        return (a | t | c | g) == 0


def load(filename):
    data = get_file(filename)
    data = parse(Sequence, "{id}:{seq}", data)
    for seq in data:
        seq.init()
    return data


def task1(data):
    [parent1, parent2, child] = data
    return child.common(parent1) * child.common(parent2)


def find_parents(data, child_info, child):
    for i in range(len(data)):
        if child_info[i]:
            continue
        p1 = data[i]
        if p1 == child:
            continue
        for j in range(len(data)):
            if child_info[j]:
                continue
            p2 = data[j]
            if p2 == child:
                continue
            if p1 == p2:
                continue
            if child.parents(p1, p2):
                return i, j
    return None


def task2(data):
    result = 0
    child = [False] * len(data)
    for i in range(len(data)):
        elem = data[i]
        parents = find_parents(data, child, elem)
        if parents is None:
            continue
        child[i] = True
        [i1, i2] = parents
        result += elem.common(data[i1]) * elem.common(data[i2])
    return result


def task3(data):
    child = [False] * len(data)
    parent_list = [None] * len(data)
    for i in range(len(data)):
        elem = data[i]
        parents = find_parents(data, child, elem)
        if parents is not None:
            parent_list[i] = parents
    print([(p[0]+1, p[1]+1) if p else None for p in parent_list])
    leaves = []
    for i in range(len(data)):
        leaf = True
        for parents in parent_list:
            if parents and i in parents:
                leaf = False
                break
        if leaf:
            leaves.append(i)

    family = [-1] * len(data)
    for i in leaves:
        family[i] = i
        stack = [i]
        while len(stack) > 0:
            elem = stack.pop()
            if family[elem] > 0:
                a = family[i]
                for j in range(len(data)):
                    if family[j] == a:
                        family[j] = family[elem]
            family[elem] = family[i]
            parents = parent_list[elem]
            if not parents:
                continue
            [p1, p2] = parents
            stack.append(p1)
            stack.append(p2)

    result = 0
    cmn = Counter(family).most_common(1)[0][0]
    for i, fam in enumerate(family):
        if fam == cmn:
            result += i+1
    return result


app = AdventDay()
app.run()
