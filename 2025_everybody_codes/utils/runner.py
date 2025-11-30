import inspect
import re
import os
from pathlib import Path


class AdventDay:
    def run(
            self,
            day: int | None = None,
            *,
            test: bool = False,
    ):
        caller_frame = inspect.currentframe().f_back
        caller_globals = caller_frame.f_globals
        if not day:
            full_path = caller_frame.f_code.co_filename
            filename = os.path.basename(full_path)
            name_without_ext = os.path.splitext(filename)[0]
            match = re.search(r'(\d+)$', name_without_ext)
            if match:
                day = int(match.group(1))

        load_func = caller_globals.get('load')

        tasks = []
        loaders = {}
        for name, obj in caller_globals.items():
            if callable(obj):
                match = re.match(r'^(part|task|star)(\d+)$', name)
                if match:
                    number = int(match.group(2))
                    tasks.append((number, name, obj))
                else:
                    match = re.match(r'^load(\d+)$', name)
                    if match:
                        number = int(match.group(1))
                        loaders[number] = obj

        tasks.sort(key=lambda x: x[0])

        if not tasks:
            print("No partN or taskN functions found.")
            return

        for number, name, func in tasks:
            print(f"--- Running {name} ---")
            try:
                data = load_data(day, number, load_func, loaders, test)
                if data:
                    sig = inspect.signature(func)
                    accepts_args = len(sig.parameters) > 0
                    if not accepts_args:
                        result = func()
                    elif type(data) is tuple:
                        result = func(*data)
                    else:
                        result = func(data)
                else:
                    result = func()

                print(f"Output: {result}")
                print("---------------------")
            except TypeError as e:
                print(f"Error running {name}: {e}")
            except FileNotFoundError as e:
                print("No file found")
                print(f"Error running {name}: {e}")


def load_data(day, number, load_func, loaders, test):
    loader = load_func
    if number in loaders:
        loader = loaders[number]
    if not loader:
        return None
    sig = inspect.signature(loader)
    if len(sig.parameters) == 0:
        return loader()
    first_param = next(iter(sig.parameters.values()))
    if first_param.annotation is int:
        return loader(number)
    if test:
        url = f"data/day{day}/example{number}"
        path = Path(url)
        if not path.exists():
            url = f"data/day{day}/example"
    else:
        url = f"data/day{day}/data{number}"
        path = Path(url)
        if not path.exists():
            url = f"data/day{day}/data"
    return loader(url)
