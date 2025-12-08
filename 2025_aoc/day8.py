from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    data = get_file(filename, strip=True)
    return [tuple(int(item) for item in x.split(',')) for x in data]


def distance_3d(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    dx_sq = (x2 - x1) ** 2
    dy_sq = (y2 - y1) ** 2
    dz_sq = (z2 - z1) ** 2
    # squared distance
    return dx_sq + dy_sq + dz_sq


def sort_by_dist(data, reversed=True):
    a = set()
    for p1 in data:
        for p2 in data:
            if p1 >= p2:
                continue
            r = (p1, p2, distance_3d(p1, p2))
            a.add(r)
    a = list(a)
    a.sort(key=lambda x: x[2], reverse=reversed)
    return a


def task1(data):
    circuits = []
    data = sort_by_dist(data)
    for i in range(1000):
        p1, p2, _ = data.pop()
        merge = []
        for num, circuit in enumerate(circuits):
            if p1 in circuit or p2 in circuit:
                merge.append(num)
        added = len(merge) > 0
        new = set()
        while len(merge) > 0:
            to_merge = merge.pop()
            to_add = circuits[to_merge]
            circuits[to_merge] = circuits[-1]
            circuits.pop()
            new.update(to_add)
            if p1 not in new:
                new.add(p1)
            if p2 not in new:
                new.add(p2)
        if len(new) > 0:
            circuits.append(new)
        if not added:
            circuits.append(set([p1, p2]))

    lens = (len(c) for c in circuits)
    to_calc = sorted(lens)[::-1][:3]
    result = 1
    for i in to_calc:
        result *= i
    return result


app = AdventDay()
app.run(test=False)
