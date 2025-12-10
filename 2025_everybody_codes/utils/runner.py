import inspect
import re
import os
from pathlib import Path
from typing import Callable, Any


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


def load_data(
        day: int, part_num: int,
        loader: Callable,
        loaders,
        test: bool
) -> Any:
    if part_num in loaders:
        loader = loaders[part_num]

    url = find_file(day, part_num, test)

    # case 1: guess how to load
    if not loader:
        return guess_loading_format(url)

    sig = inspect.signature(loader)
    if len(sig.parameters) == 0:
        return loader()

    first_param = next(iter(sig.parameters.values()))
    # case 2: user wants only part number
    if first_param.annotation is int:
        return loader(part_num)

    # case 3: user wants filename
    if not url:
        raise FileNotFoundError()
    if first_param.annotation is str:
        return loader(str(part_num))
    return loader(url)


def find_file(day: int, part_num: int, test: bool) -> Path | None:
    filenames = []

    if test:
        filenames = [
            f"example{part_num}", f"test{part_num}",
        ]
    else:
        filenames = [
            f"input{part_num}", f"data{part_num}",
            f"{day}"
        ]

    base_dir = Path('')
    search_paths = [
        base_dir / "data" / f"day{day}",
        base_dir / "inputs" / f"day{day}",
    ]

    for path in search_paths:
        for fname in filenames:
            candidate = path / fname
            if candidate.exists():
                return candidate

    fallback = f"data/day{day}/{'example' if test else 'data'}"
    fallback_file = Path(fallback)
    if fallback_file.exists():
        return fallback_file
    return None


def guess_loading_format(filename: Path | str | None) -> Any:
    if not filename:
        return None
    if type(filename) is str:
        filename = Path(filename)
    if not Path.exists():
        return None
    if not Path.is_file():
        return None

    # TODO
    return filename.read_text().strip()
