import inspect
import re
import os
from pathlib import Path
from typing import Callable, Any
import time
from .term import Term
from dataclasses import dataclass


@dataclass
class Solver:
    part: int
    name: str
    func: Callable


@dataclass
class TestCase:
    expected: Any
    input_data: str | None = None
    input_file: str | None = None
    only_for: str | list[str] | None = None
    description: str = "Test Case"


class AdventDay:
    def __init__(self, day: int = None, year: int = None):
        self._day = day
        self._year = year
        self._base_path = Path.cwd()
        self.term = Term()

        self.tasks: list[Solver] = []
        self.tests: dict[int, list[TestCase]] = {}
        self.loaders = {}
        self.loader = None

    def run(
            self,
            day: int | None = None,
            *,
            test: bool = False,
    ):
        caller_frame = inspect.currentframe().f_back
        day = day if day else self._detect_day(caller_frame.f_code.co_filename)
        term = self.term

        self._discover_functions(caller_frame.f_globals)
        self._update_tests_from_annotations()

        print(f"Advent of Code {self._year or ''} // day {day:02d}".upper())
        term.dim()
        term.print("» Mode: ")
        if test:
            term.magenta()
            term.println('TEST')
        else:
            term.red()
            term.println('REAL')
        term.dim()
        term.print("» Solvers: ")
        term.println(len(self.tasks))
        print()

        if not self.tasks:
            term.red()
            term.println("No solvers found. Add partN or solveN functions")
            return

        # TODO: group by part_num
        for task in self.tasks:
            part_num = task.part
            name = task.name
            func = task.func
            term.bold()
            term.blue()
            term.println(f"─── {name.upper()} ───")
            try:
                data = load_data(
                        day, part_num, self.loader, self.loaders, test
                )
            except TypeError as e:
                print(f"Error running {name}: {e}")
            except FileNotFoundError as e:
                print("No file found")
                print(f"Error running {name}: {e}")

            self.run_part(func, data, part_num)
            print()

    def run_part(
            self, func: Callable, data: Any, part: int
    ):
        sig = inspect.signature(func)
        accepts_args = len(sig.parameters) > 0

        # TODO: run test

        start_time = time.perf_counter_ns()
        result = None
        try:
            result = self.run_single(func, accepts_args, data)
        except Exception as e:
            self.term.fatal(e)
        end_time = time.perf_counter_ns()
        duration = end_time - start_time

        if result:
            self.term.ok("Result", result)
        self.term.dim()
        self.term.println(f"Time: {Term.format_time(duration)}")

    def run_single(self, func: Callable, accepts_args: bool, data: Any):
        if not data:
            return func()
        if not accepts_args:
            return func()
        elif type(data) is tuple:
            return func(*data)
        return func(data)

    def _detect_day(self, frame_filename: str) -> int:
        if self._day:
            return self._day
        filename = os.path.basename(frame_filename)
        name_without_ext = os.path.splitext(filename)[0]
        match = re.search(r'(\d+)$', name_without_ext)
        if match:
            return int(match.group(1))
        print("Warning: Could not auto-detect day number. Defaulting to 0.")
        return 0

    def _discover_functions(self, scope: dict[str, Any]):
        self.loaders = {}

        for name, obj in scope.items():
            if not callable(obj):
                continue
            task_match = re.match(
                    r'^(?:part|task|star)(\d+)$',
                    name, re.IGNORECASE
            )
            if task_match:
                number = int(task_match.group(1))
                self._add_solver(number, name, obj)
                continue
            load_match = re.match(r'^load(\d+)$', name)
            if load_match:
                number = int(load_match.group(1))
                self.loaders[number] = obj

        self.tasks.sort(key=lambda x: x.part)

        self.loader = scope.get('load')

    def _add_solver(self, part: int, name: str, func: Callable) -> Solver:
        self.tasks.append(Solver(part=part, name=name, func=func))

    def task(self, part: int = None):
        def decorator(func):
            p = part
            if p is None:
                match = re.search(r'(\d+)', func.__name__)
                if match:
                    p = int(match.group(1))
                else:
                    raise ValueError("Cannot resolve part number for {func.__name__}, please provide part argument.")
            self._add_solver(p, func.__name__, func)
            return func
        return decorator

    def test(
            self, expected: Any, input: str = None,
            file: str = None, desc: str = None,
            only_for: str | list[str] | None = None
    ):
        def decorator(func):
            if not hasattr(func, '_advent_tests'):
                func._advent_tests = []
            case = TestCase(
                    expected=expected,
                    input_data=input,
                    input_file=file,
                    only_for=only_for,
                    description=desc or f"Test #{len(func._advent_tests)+1}"
            )
            func._advent_tests.insert(0, case)
            return func
        return decorator

    def _update_tests_from_annotations(self):
        for task in self.tasks:
            if not hasattr(task, '_advent_tests'):
                continue
            if self.tests.get(task.part) is None:
                self.tests.set(task.part, [])
            tests = self.tests.get(task.part)
            tests.extend(task._advent_tests)

    def _select_loader(self, day: int, part_num: int, test: bool):
        return self.loaders.get(part_num, self.loader)


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
