from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass


@dataclass
class Instr:
    id: int
    left_rank: int
    left_id: str
    right_rank: int
    right_id: str


@dataclass
class Node:
    id: str
    rank: int
    level: int = 0
    left: "Node | None" = None
    right: "Node | None" = None

    def put(self, other: "Node") -> int:
        if other.rank < self.rank:
            if not self.left:
                self.left = other
                other.level = self.level + 1
                return self.level + 1
            else:
                return self.left.put(other)
        elif other.rank > self.rank:
            if not self.right:
                self.right = other
                other.level = self.level + 1
                return self.level + 1
            else:
                return self.right.put(other)

    def get(self, level: int) -> str:
        if self.level == level:
            return self.id
        else:
            left = self.left.get(level) if self.left else ''
            right = self.right.get(level) if self.right else ''
            return left+right



def load(filename) -> list[Instr]:
    return parse(
            Instr,
            "ADD id={id} left=[{left_rank},{left_id}] right=[{right_rank},{right_id}]",
            get_file(filename),
            list_separator=','
            )


def task1(data):
    inst = data[0]
    left_tree = Node(id=inst.left_id, rank=inst.left_rank)
    right_tree = Node(id=inst.right_id, rank=inst.right_rank)
    l_levels = {}
    r_levels = {}
    for instr in data[1:]:
        left = Node(id=instr.left_id, rank=instr.left_rank)
        right = Node(id=instr.right_id, rank=instr.right_rank)
        lvl = left_tree.put(left)
        l_levels.setdefault(lvl, 0)
        l_levels[lvl] += 1
        lvl = right_tree.put(right)
        r_levels.setdefault(lvl, 0)
        r_levels[lvl] += 1

    max_l_level = max(l_levels, key=l_levels.get)
    max_r_level = max(r_levels, key=r_levels.get)
    return left_tree.get(max_l_level) + right_tree.get(max_r_level)


app = AdventDay()
app.run()
