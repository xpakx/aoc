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


app = AdventDay()
app.run()
