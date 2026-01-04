from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    data = get_file(filename)
    targets = []
    segments = {}
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == 'T':
                targets.append((i, j))
            elif cell == 'H':
                targets.append((i, j))
                targets.append((i, j))
            elif cell not in ['.', '=']:
                segments[cell] = (i, j)
    return targets, segments


def task1(targets, segments):
    result = 0
    for t0, t1 in targets:
        for key, (s0, s1) in segments.items():
            #   s0 - power + n == t0
            #   s1 + 2*power + n == t1
            # - ---------------------
            #   s0-s1 - 3*power = t0 - t1
            #   -3*power = t0-t1-s0+s1
            #   3*power = t1+s0-s1-t0
            power = t1+s0-s1-t0
            if power/3 == power//3:
                print(key, power//3, ord(key)-64)
                result += (power//3)*(ord(key)-64)
        print()
    print(targets)
    print(segments)
    return result


def task2(targets, segments):
    result = 0
    for t0, t1 in targets:
        for key, (s0, s1) in segments.items():
            power = t1+s0-s1-t0
            if power/3 == power//3:
                print(key, power//3, ord(key)-64)
                result += (power//3)*(ord(key)-64)
        print()
    print(targets)
    print(segments)
    return result


def load3(filename):
    data = get_file(filename)
    return [tuple([int(y) for y in x.split()]) for x in data]


def draw(data, segments):
    for j in range(10):
        for i in range(13):
            x = i
            y = 9 - j
            if (x, y) in data:
                print('#', end='')
            elif (x, y) in segments.values():
                for k, s in segments.items():
                    if s == (x, y):
                        print(k, end='')
                        break
            else:
                print('.', end='')
        print()


def try_to_fit(elem, segments, candidates, steps):
    for key, segment in segments.items():
        # print(key)
        d0 = elem[0] - segment[0]
        d1 = elem[1] - segment[1]
        if d1 > d0:
            # print('over', key, elem)
            continue
        len = 0
        power = 0
        if d0 == d1:
            len = d0
            power = len
            # print(d0, d1)
        elif d0 <= 2*d1 and d1 > 0:
            power = d1
            len = d0
            # print(d0, d1)
        else:
            #   s1 + power - n == t1
            #   s0 + 2*power + n == t0
            # + ---------------------
            #   s1+s0 + 3*power = t1 + t0
            #   3*power = t1+t1-s0-s1
            power = elem[0]+elem[1]-segment[1]-segment[0]
            # print(power)
            if power/3 == power//3:
                power = power // 3
                # print(power)
                # n = t0-s0-2*power
                n = elem[0] - segment[0] - 2*power
                # print("n", n)
                len = 2*power + n
        # print(len)
        if len > 0 and len <= steps:
            score = power*(ord(key)-64)
            print(key, power, len, score)
            # draw([elem], segments)
            candidates.append(score)


def part3(data):
    segments = {'A': (0, 0), 'B': (0, 1), 'C': (0, 2)}
    result = 0
    for elem in data:
        steps = 0
        found = False
        candidates = []
        while not found:
            candidates = []
            steps += 1
            elem = (elem[0]-1, elem[1]-1)
            # draw([elem], segments)
            # print()
            try_to_fit(elem, segments, candidates, steps)
            if len(candidates) > 0:
                found = True
            # print(candidates)
        result += min(candidates)
        print(min(candidates))

    draw([elem], segments)
    print(data)
    return result


app = AdventDay()
app.run()
