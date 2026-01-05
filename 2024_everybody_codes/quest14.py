from utils.loader import get_file
from utils.runner import AdventDay
import heapq


def load(filename):
    data = get_file(filename)
    return [prepare_branch(x) for x in data]


def prepare_branch(data):
    data = data.split(',')
    instr = []
    for entry in data:
        dir = entry[0]
        steps = int(entry[1:])
        if dir in ['B', 'D', 'R']:
            steps = -steps
        if dir in ['L', 'R']:
            instr.append((steps, 0, 0))
        if dir in ['D', 'U']:
            instr.append((0, steps, 0))
        if dir in ['F', 'B']:
            instr.append((0, 0, steps))
    return instr


def task1(data):
    height = 0
    max = 0
    for _, y, _ in data[0]:
        height += y
        if height > max:
            max = height
    return max


def add_segments(segments, start, step):
    if step[0] != 0:
        s = step[0]
        r = range(min(0, s), max(0, s)+1)
        print(r, step, start)
        print([(start[0]+x, start[1], start[2]) for x in r])
        segments.update([(start[0]+x, start[1], start[2]) for x in r])
    elif step[1] != 0:
        s = step[1]
        r = range(min(0, s), max(0, s)+1)
        print(r, step, start)
        print([(start[0], start[1]+x, start[2]) for x in r])
        segments.update([(start[0], start[1]+x, start[2]) for x in r])
    else:
        s = step[2]
        r = range(min(0, s), max(0, s)+1)
        print(r, step, start)
        print([(start[0], start[1], start[2]+x) for x in r])
        segments.update([(start[0], start[1], start[2]+x) for x in r])


def task2(data):
    segments = set()
    start = (0, 0, 0)
    for branch in data:
        seg = start
        for x, y, z in branch:
            add_segments(segments, seg, (x, y, z))
            seg = (seg[0]+x, seg[1]+y, seg[2]+z)
    return len(segments)-1


def add_to_trunk(trunk, start, step):
    if step[0] != 0:
        if step[2] != 0:
            return
        p1 = min(start[0], start[0]+step[0])
        p2 = max(start[0], start[0]+step[0])
        if p1 <= 0 and p2 >= 0:
            trunk.add(start[1])
    elif step[1] != 0:
        if start[0] != 0 or start[1] != 0:
            return
        s = step[1]
        r = range(min(0, s), max(0, s)+1)
        trunk.update([start[1]+x for x in r])
    elif step[2] != 0:
        if step[0] != 0:
            return
        p1 = min(start[2], start[2]+step[2])
        p2 = max(start[2], start[2]+step[2])
        if p1 <= 0 and p2 >= 0:
            trunk.add(start[1])


dirs = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]


def neighbors(elem):
    return [(elem[0]+i, elem[1]+j, elem[2]+k) for i, j, k in dirs]


def to_value(symbol):
    if symbol in ['S', 'E']:
        return 0
    return ord(symbol)-48


def find_path(start, segments, leaf):
    queue = [(0, start)]
    heapq.heapify(queue)
    min_costs = {start: 0}
    while queue:
        cost, curr = heapq.heappop(queue)
        if curr == leaf:
            return cost
        for neighbor in neighbors(curr):
            if neighbor not in segments:
                continue
            if cost + 1 < min_costs.get(neighbor, float('inf')):
                min_costs[neighbor] = cost + 1
                heapq.heappush(queue, (cost+1, neighbor))


def task3(data):
    start = (0, 0, 0)
    leaves = set()
    trunk = set()
    segments = set()
    for branch in data:
        seg = start
        for x, y, z in branch:
            add_to_trunk(trunk, seg, (x, y, z))
            add_segments(segments, seg, (x, y, z))
            seg = (seg[0]+x, seg[1]+y, seg[2]+z)
        leaves.add(seg)
    print(leaves)
    print(trunk)

    min_score = float('inf')
    scores = []
    h = -1
    for height in trunk:
        score = 0
        lst = []
        for leaf in leaves:
            leaf_score = find_path((0, height, 0), segments, leaf)
            if leaf_score is None:
                score = float('inf')
                continue
            score += leaf_score
            lst.append(leaf_score)
        if score < min_score:
            min_score = score
            scores = lst
            h = height
    print(scores, h)
    return min_score


app = AdventDay()
app.run()
