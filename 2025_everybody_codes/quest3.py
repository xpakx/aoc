from pathlib import Path
from collections import Counter
from utils.runner import AdventDay


def load(filename):
    data = Path(filename).read_text(encoding='utf-8').split(',')
    data = list(map(lambda n: int(n), data))
    data.sort(reverse=True)
    return data


def task1(data):
    last = data[0]+1000
    result = 0
    for i in data:
        if i < last:
            last = i
            result += i
    return result


def task2(data):
    data = list(dict.fromkeys(data))
    return sum(data[-20:])


def task3(data):
    cnt = Counter(data)
    print(cnt)
    return max(cnt.values())


app = AdventDay()
app.run()
