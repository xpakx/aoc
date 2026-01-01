from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, as_int=True)


def get_stamp(brigthness, stamps):
    for i, stamp in enumerate(stamps):
        if brigthness < stamp:
            return stamps[i-1]
    return stamps[i]


def stamps_for(brigthness, stamps):
    used = []
    while brigthness > 0:
        stamp = get_stamp(brigthness, stamps)
        brigthness -= stamp
        used.append(stamp)
    return used


def task1(brightness):
    stamps = [1, 3, 5, 10]
    result = 0
    for b in brightness:
        s = stamps_for(b, stamps)
        print(b, s)
        result += len(s)
    return result


app = AdventDay()
app.run()
