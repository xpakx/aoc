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

    def put(self, other: "Node"):
        if other.rank < self.rank:
            if not self.left:
                self.left = other
                other.level = self.level + 1
            else:
                self.left.put(other)
        elif other.rank > self.rank:
            if not self.right:
                self.right = other
                other.level = self.level + 1
            else:
                self.right.put(other)


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
    for instr in data[1:]:
        left = Node(id=instr.left_id, rank=instr.left_rank)
        right = Node(id=instr.right_id, rank=instr.right_rank)
        left_tree.put(left)
        right_tree.put(right)

    print(left_tree)


app = AdventDay()
app.run()
