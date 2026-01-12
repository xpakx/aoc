from utils.loader import get_file
from utils.runner import AdventDay


def load(filename) -> list[str]:
    return get_file(filename)


def task1(data: list[str]):
    print(data)


app = AdventDay()
app.run()
