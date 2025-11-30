from utils.loader import get_file
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass


@dataclass
class Spine:
    num: int
    left: int | None = None
    right: int | None = None

    def place(self, num: int) -> bool:
        if num < self.num and self.left is None:
            self.left = num
            return True
        if num > self.num and self.right is None:
            self.right = num
            return True
        return False

    def calculate_quality(self):
        val = []
        if self.left:
            val.append(self.left)
        val.append(self.num)
        if self.right:
            val.append(self.right)
        q = ''.join(map(lambda s: str(s), val))
        self.quality = int(q)


@dataclass
class Sword:
    id: int
    nums: list[int]

    def construct(self):
        self.spine = construct(self)
        q = ''.join(map(lambda s: str(s.num), self.spine))
        self.quality = int(q)
        return self.quality

    def quality_for_spines(self):
        for sp in self.spine:
            sp.calculate_quality()

    def __eq__(self, other):
        return False

    def __lt__(self, other):
        if self.quality != other.quality:
            return self.quality < other.quality
        for i in range(len(self.spine)):
            self_spine = self.spine[i].quality
            other_spine = other.spine[i].quality
            if self_spine != other_spine:
                return self_spine < other_spine
        return self.id < other.id


def load(filename):
    data = get_file(filename, split_lines=False)
    return parse(Sword, "{id}:{nums}", data, list_separator=',')


def construct(sword):
    spine = [Spine(num=sword.nums[0])]
    for num in sword.nums[1:]:
        placed = False
        for elem in spine:
            succ = elem.place(num)
            if succ:
                placed = True
                break
        if not placed:
            spine.append(Spine(num=num))
    return spine


def task1(data):
    print(data)
    sword = data[0]
    sword.construct()
    return sword.quality


def task2(data):
    min = 10000000000000000000000000000
    max = 0
    for sword in data:
        sword.construct()
        quality = sword.quality
        if quality < min:
            min = quality
        if quality > max:
            max = quality
    print(max, min)
    return max - min


def task3(data):
    for sword in data:
        sword.construct()
        sword.quality_for_spines()
    data = reversed(sorted(data))
    result = 0
    for i, s in enumerate(data):
        result += s.id * (i+1)
    return result


app = AdventDay()
app.run()
