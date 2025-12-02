from utils.loader import get_file_instr
from utils.runner import AdventDay
from utils.parser import parse
from dataclasses import dataclass


@dataclass
class Rule:
    first: str
    to: list[str]


def load(filename):
    [names, rules] = get_file_instr(filename, split_second_by="\n")
    rules = parse(Rule, "{first} > {to}", rules, list_separator=",")
    return names, rules


def task1(names, rules):
    print(names)
    print(rules)
    r = {}
    for rule in rules:
        r[rule.first] = rule.to
    for name in names:
        correct = True
        for i in range(len(name)-1):
            curr_letter = name[i]
            next_letter = name[i+1]
            candidates = r[curr_letter]
            if not candidates or next_letter not in candidates:
                correct = False
                break
        if correct:
            return name


def task2(names, rules):
    r = {}
    for rule in rules:
        r[rule.first] = rule.to
    result = 0
    for j in range(len(names)):
        name = names[j]
        correct = True
        for i in range(len(name)-1):
            curr_letter = name[i]
            next_letter = name[i+1]
            candidates = r[curr_letter]
            if not candidates or next_letter not in candidates:
                correct = False
                break
        if correct:
            result += j + 1
    return result


def task3(names, rules):
    r = {}
    for rule in rules:
        r[rule.first] = rule.to

    options = set()
    visited = set()
    for name in sorted(names, key=len):
        correct = True
        for i in range(len(name)-1):
            curr_letter = name[i]
            next_letter = name[i+1]
            candidates = r[curr_letter]
            if not candidates or next_letter not in candidates:
                correct = False
                break
        if not correct:
            continue
        letter = name[-1]
        candidates = [name + x for x in r[letter]]
        print(name)

        while len(candidates) != 0:
            suffix = candidates.pop()
            if suffix in visited:
                continue
            visited.add(suffix)
            if len(suffix) > 11:
                continue
            if len(suffix) >= 7:
                options.add(suffix)
            letter = suffix[-1]
            if letter not in r:
                continue
            new_letters = [suffix + x for x in r[letter]]
            candidates.extend(new_letters)

    return len(options)


app = AdventDay()
app.run()
