from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, split_by=",", split_lines=False, as_int=True)


def task1(data):
    nails = max(data)
    step = nails // 2
    result = 0
    for i, j in zip(data, data[1:]):
        if abs(j - i) == step:
            result += 1
    return result


def check_sides(s1, s2, nails):
    if s1[0] == s2[0] or s1[0] == s2[1]:
        return False
    if s1[1] == s2[0] or s1[1] == s2[1]:
        return False
    s11OnSideA = s1[0] > s2[0] and s1[0] < s2[1]
    s12nSideA = s1[1] > s2[0] and s1[1] < s2[1]
    return s11OnSideA != s12nSideA


def task2(data):
    nails = max(data)
    result = 0
    segments = []
    for i, j in zip(data, data[1:]):
        segment = [min(i, j), max(i, j)]
        for s in segments:
            if check_sides(segment, s, nails):
                result += 1
        segments.append(segment)
    return result


def task3(data):
    nails = max(data)
    result = 0
    segments = [[min(i, j), max(i, j)] for i, j in zip(data, data[1:])]
    for i in range(nails):
        for j in range(nails):
            if i == j:
                continue
            r = 0
            seg = [min(i, j)+1, max(i, j)+1]
            for s in segments:
                if check_sides(seg, s, nails):
                    r += 1
            if seg in segments:
                r += 1
            if r > result:
                result = r
    return result


app = AdventDay()
app.run()
