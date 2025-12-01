from utils.loader import get_file
from utils.runner import AdventDay
from collections import defaultdict


def load(filename):
    data = get_file(filename, split_lines=False)
    return data


def task1(data):
    result = 0
    mentors = 0
    for c in data:
        if c == 'A':
            mentors += 1
        elif c == 'a':
            result += mentors
    return result


def task2(data):
    result = 0
    mentors = defaultdict(int)
    for c in data:
        if c.isupper():
            mentors[c.lower()] += 1
        elif c.islower():
            result += mentors[c]
    return result


def print_bin(num):
    print(''.join(reversed(format(num, '#030b')[2:])))


# doesn't work on example bc len(data) < dist
# prolly sliding window would be a better approach
def task3(data):
    dist = 1000
    rep = 1000
    ln = len(data)*rep
    print(ln)
    letter_masks = defaultdict(int)
    for i in range(len(data)):
        c = data[i % len(data)]
        if c.isupper():
            m = letter_masks[c.lower()]
            m ^= 1 << i
            letter_masks[c.lower()] = m

    result = 0
    result_prev = 0
    result_next = 0
    mask = (1 << dist+1) - 1
    prev_mask = ((1 << dist) - 1) << (len(data) - dist)
    next_mask = 0
    for i in range(len(data)):
        c = data[i % len(data)]
        if c.islower():
            m = letter_masks[c]
            r = m & mask
            result += r.bit_count()
            r = m & prev_mask
            result_prev += r.bit_count()
            r = m & next_mask
            result_next += r.bit_count()
        mask <<= 1
        prev_mask <<= 1
        next_mask <<= 1
        if i < dist:
            mask ^= 1
        if i >= len(data) - dist - 1:
            next_mask ^= 1

    if rep == 1:
        return result
    first_pass = result + result_next
    last_pass = result_prev + result
    other_pass = result_prev + result + result_next
    return first_pass + last_pass + max(0, rep-2)*other_pass


app = AdventDay()
app.run()
