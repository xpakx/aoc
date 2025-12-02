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


app = AdventDay()
app.run()
