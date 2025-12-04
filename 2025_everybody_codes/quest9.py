from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass


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


def load(filename):
    data = get_file(filename)
    data = parse(Sequence, "{id}:{seq}", data)
    for seq in data:
        seq.init()
    return data


def task1(data):
    [parent1, parent2, child] = data
    return child.common(parent1) * child.common(parent2)


app = AdventDay()
app.run()
