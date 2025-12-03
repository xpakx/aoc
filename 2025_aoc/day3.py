from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename)


def task1(data):
    result = 0
    for rating in data:
        max = 0
        next = 0
        for i in range(len(rating)):
            c = rating[i]
            num = ord(c) - 48
            if num > max and i < len(rating)-1:
                max = num
                next = 0
            elif num > next:
                next = num
        result += max*10 + next
    return result


def task2(data):
    result = 0
    for rating in data:
        number = [0]*12
        for i in range(len(rating)):
            c = rating[i]
            num = ord(c) - 48
            for j in range(len(number)):
                n = number[j]
                if num > n and i < len(rating) - (12-j) + 1:
                    number[j] = num
                    for k in range(j+1, len(number)):
                        number[k] = 0
                    break
        for i, n in enumerate(reversed(number)):
            result += n*10**i
    return result


app = AdventDay()
app.run()
