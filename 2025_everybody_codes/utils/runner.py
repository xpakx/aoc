import inspect
import re


class AdventDay:
    def run(self):
        caller_frame = inspect.currentframe().f_back
        caller_globals = caller_frame.f_globals

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
                load_spec = None
                if number in loaders:
                    load_spec = loaders[number]
                if load_func or load_spec:
                    if load_spec:
                        data = load_spec()
                    else:
                        data = load_func(number)
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
