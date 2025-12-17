import inspect
import re
import os
from pathlib import Path
from typing import Callable, Any
import time
from .term import Term
from dataclasses import dataclass
import argparse
import builtins
import io


@dataclass
class Solver:
    part: int
    name: str
    func: Callable
    alt: bool = False


@dataclass
class TestCase:
    expected: Any
    input_data: str | None = None
    input_file: str | None = None
    only_for: str | list[str] | None = None
    description: str = "Test Case"


@dataclass
class RunResult:
    result: Any
    time: int


class AdventDay:
    def __init__(self, day: int = None, year: int = None):
        self._day = day
        self._year = year
        self._base_path = Path.cwd()
        self.term = Term()
        self.example_mode = None
        self.compare = False
        self.run_tests = False

        self.tasks: dict[int, list[Solver]] = {}
        self.tests: dict[int, list[TestCase]] = {}
        self.loaders = {}
        self.loader = None
        self.day = None

    def run(
            self,
            day: int | None = None,
            *,
            test: bool = False,
    ):
        caller_frame = inspect.currentframe().f_back
        day = day if day else self._detect_day(caller_frame.f_code.co_filename)
        self.day = day
        term = self.term

        self._discover_functions(caller_frame.f_globals)
        self._update_tests_from_annotations()

        self._detect_arguments()
        if self.example_mode is not None:
            test = self.example_mode

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
        # TODO
        solver_count = sum(
                len(list_value) for list_value in self.tasks.values()
        )
        term.println(solver_count)
        print()

        if solver_count == 0:
            term.red()
            term.println("No solvers found. Add partN or solveN functions")
            return

        for part in sorted(self.tasks.keys()):
            tasks = self.tasks[part]
            term.bold()
            term.blue()
            solver_main = self._select_main_solver(tasks, part)
            term.println(f"─── PART {part} ───")
            result = self.run_part(solver_main, test)
            if result.result:
                self.term.ok("Result", result.result)
            self.term.dim()
            self.term.println(f"Time: {Term.format_time(result.time)}")
            if self.compare:
                self.run_alts(solver_main, result, tasks, test)
            print()

    def run_part(
            self,
            solver: Solver,
            test: bool,
    ) -> RunResult:
        func = solver.func
        name = solver.name
        part = solver.part
        try:
            data = load_data(
                    self.day, part, self.loader, self.loaders, test
            )
        except TypeError as e:
            print(f"Error running {name}: {e}")
        except FileNotFoundError as e:
            print("No file found")
            print(f"Error running {name}: {e}")

        sig = inspect.signature(func)
        accepts_args = len(sig.parameters) > 0

        if self.run_tests:
            self._run_tests(func, part)

        start_time = time.perf_counter_ns()
        result = None
        try:
            result = self.run_single(func, accepts_args, data)
        except Exception as e:
            self.term.fatal(e)
        end_time = time.perf_counter_ns()
        duration = end_time - start_time

        return RunResult(result=result, time=duration)

    def run_single(self, func: Callable, accepts_args: bool, data: Any):
        if not data:
            return func()
        if not accepts_args:
            return func()
        elif type(data) is tuple:
            return func(*data)
        return func(data)

    def run_alts(
            self, main: Solver, main_result: RunResult,
            solvers: list[Solver], test: bool
    ):
        self.term.indent(2)
        for solver in solvers:
            if main == solver:
                continue
            result = self.run_part(solver, test)
            self.term.print("└ ")
            self.term.dim()
            self.term.print(f"Alt {solver.name}")
            self.term.print(": ")
            if result.result == main_result.result:
                self.term.green()
                self.term.print("✔ ")
            else:
                self.term.red()
                self.term.print("✖ ")
                self.term.dim()
                self.term.print(f"(Got: {result.result}) ")

            self.term.print(f"{self.term.format_time(result.time)} ")
            if result.time < main_result.time:
                factor = main_result.time / result.time
                self.term.green()
                self.term.print(f"[{factor:.1f}x faster]")
            elif main_result.time < result.time:
                factor = result.time / main_result.time
                self.term.red()
                self.term.print(f"[{factor:.1f}x slower]")

        self.term.dedent(2)

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

        self.loader = scope.get('load')

    def _add_solver(self, part: int, name: str, func: Callable) -> Solver:
        if part not in self.tasks:
            self.tasks[part] = []
        self.tasks[part].append(Solver(part=part, name=name, func=func))

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
        for tasks in self.tasks.values():
            for task in tasks:
                if not hasattr(task.func, '_advent_tests'):
                    continue
                if self.tests.get(task.part) is None:
                    self.tests[task.part] = []
                tests = self.tests.get(task.part)
                tests.extend(task.func._advent_tests)

    def _select_loader(self, day: int, part_num: int, test: bool):
        return self.loaders.get(part_num, self.loader)

    def _run_tests(self, func: Callable, part_num: int):
        tests = self.tests.get(part_num)
        if not tests:
            return
        sig = inspect.signature(func)
        accepts_args = len(sig.parameters) > 0
        self.term.dim()
        self.term.println(f"Running {len(tests)} inline "
                          f"test{'s' if len(tests) > 1 else ''}...")
        self.term.indent(2)

        for test in tests:
            data = self._get_test_data(test)
            all_passed = True
            err = False
            actual = None
            try:
                actual = self.run_single(func, accepts_args, data)
            except Exception as e:
                self.term.fail(test.description, f"Error: {e}")
                err = True
                all_passed = False
            is_pass = actual == test.expected
            if is_pass:
                self.term.green()
                self.term.println(f"✔ {test.description} ")
            elif not err:
                self.term.red()
                self.term.print(f"✘ {test.description} ")
                self.term.dim()
                self.term.print("| ")
                self.term.dim()
                self.term.print(f"Expected: {test.expected} /")
                self.term.dim()
                self.term.println(f" Got: {actual}")
                all_passed = False

        if not all_passed:
            self.term.red()
            self.term.println("Tests failed")
        else:
            self.term.green()
            self.term.println("All tests passed")
        print()
        self.term.dedent(2)

    def _get_test_data(self, test: TestCase):
        if test.input_file is not None and test.input_data is not None:
            self.term.warn("Both input data and file are defined. Using file.")
        data = None
        if test.input_file:
            try:
                data = load_data(
                        self.day, 0, self.loader, self.loaders, False,
                        filename=test.input_file,
                )
            except FileNotFoundError as e:
                self.term.fatal(e)
            return data

        original_open = builtins.open
        sentinel = "__ADVENT_TEST_INPUT_DATA_SENTINEL__"
        builtins.open = generate_mock_read(
                test.input_data, sentinel, original_open
        )
        try:
            # TODO: separate getting loader and loading data
            # TODO: use correct part
            data = load_data(
                    self.day, 0, self.loader, self.loaders, False,
                    filename=sentinel,
            )
        except TypeError as e:
            print(f"Error running Test: {e}")
        except FileNotFoundError as e:
            print("No file found")
            print(f"Error running Test: {e}")
        finally:
            builtins.open = original_open
        return data

    def _detect_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
                '-e', '--example',
                action='store_true',
                help='Run on example data'
        )
        parser.add_argument(
                '-c', '--compare',
                action='store_true',
                help='Compare alternative solutions'
        )
        parser.add_argument(
                '-t', '--test',
                action='store_true',
                help='Run tests'
        )
        args = parser.parse_args()
        if args.example:
            self.example_mode = True
        self.compare = args.compare
        self.run_tests = args.test

    def _select_main_solver(
            self, solvers: list[Solver],
            part_num: int
    ) -> Solver | None:
        best_candidate = None
        prim = ["part", "task", "star"]
        primary_names = [x+str(part_num) for x in prim]
        for solver in solvers:
            if solver.name in primary_names:
                return solver
            if not solver.alt and best_candidate is None:
                best_candidate = solver
        return best_candidate


def load_data(
        day: int, part_num: int,
        loader: Callable,
        loaders,
        test: bool,
        filename: str | None = None,
) -> Any:
    if part_num in loaders:
        loader = loaders[part_num]

    url = find_file(day, part_num, test, filename)

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
    # TODO: make better way for user to request filename
    if first_param.annotation is str:
        return loader(str(url))
    return loader(url)


def find_file(
        day: int, part_num: int, test: bool,
        filename: str | None = None
) -> Path | None:
    if filename is not None:
        return filename

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
    if not filename.exists():
        return None
    if not Path.is_file():
        return None

    # TODO
    return filename.read_text().strip()


def generate_mock_read(text: str, sentinel: str, original_open):
    def mock_read(file, mode="r", encoding=None):
        if file == sentinel:
            return io.StringIO(text)
        else:
            original_open(file, mode, encoding)
    return mock_read
