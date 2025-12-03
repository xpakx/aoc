from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename)


def get_batteries(rating, batteries):
    number = [0]*batteries
    for i in range(len(rating)):
        c = rating[i]
        num = ord(c) - 48
        for j in range(len(number)):
            n = number[j]
            if num > n and i < len(rating) - (batteries-j) + 1:
                number[j] = num
                for k in range(j+1, len(number)):
                    number[k] = 0
                break
    result = 0
    for i, n in enumerate(reversed(number)):
        result += n*10**i
    return result


def task1(data):
    result = 0
    for rating in data:
        result += get_batteries(rating, 2)
    return result


def task2(data):
    result = 0
    for rating in data:
        result += get_batteries(rating, 12)
    return result


app = AdventDay()
app.run()
