class Term:
    def __init__(self):
        self.prefix = ""
        self.color_prefix = ""
        self.style_prefix = ""
        self.after_new_line = True

    def set_padding(self, level: int = 0):
        self.prefix = " " * level

    def red(self):
        self.color_prefix = Term.RED

    def magenta(self):
        self.color_prefix = Term.MAGENTA

    def blue(self):
        self.color_prefix = Term.BLUE

    def green(self):
        self.color_prefix = Term.GREEN

    def gold(self):
        self.color_prefix = Term.GOLD

    def yellow(self):
        self.color_prefix = Term.YELLOW

    def dim(self):
        self.style_prefix = Term.DIM

    def bold(self):
        self.style_prefix = Term.BOLD

    def reset_color(self):
        self.color_prefix = ""

    def reset_style(self):
        self.style_prefix = ""

    def print(self, text: str, *, end=""):
        prefix = self.prefix if self.after_new_line else ''
        print(
                f"{prefix}{self.color_prefix}{self.style_prefix}"
                f"{text}{Term.RESET}",
                end=end
        )
        self.after_new_line = (end is None)
        self.reset_style()
        self.reset_color()

    def println(self, text: str):
        self.print(text, end=None)

    def ok(self, reason: str, value: str | None = None):
        self.green()
        self.print(f"✔ {reason}{":" if value is not None else ""} ")
        if value is not None:
            if '\n' in str(value):
                self.println("(Multiline)")
            self.bold()
            self.gold()
            self.println(value)
        else:
            print()

    def fail(self, reason: str, value: str | None = None):
        self.red()
        self.bold()
        self.print(f"✘ {reason.strip()}")
        if value is not None:
            self.print(": ")
            self.println(value)
        else:
            self.println("")

    def warn(self, text: str):
        self.yellow()
        self.bold()
        self.print("⚠ Warning: ")
        self.println(text)

    def fatal(self, error: Exception):
        self.red()
        self.bold()
        self.print(f"⚠ {type(error).__name__}: ")
        self.println(str(error))

    RESET = "\033[0m"

    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    GOLD = "\033[38;5;220m"
    YELLOW = "\033[33m"

    @staticmethod
    def format_time(ns: int) -> str:
        if ns < 1000:
            return f"{ns}ns"
        elif ns < 1_000_000:
            return f"{ns / 1000:.2f}µs"
        elif ns < 1_000_000_000:
            return f"{ns / 1_000_000:.2f}ms"
        else:
            return f"{ns / 1_000_000_000:.2f}s"
