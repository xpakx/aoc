class Term:
    def __init__(self):
        self.prefix = ""
        self.color_prefix = ""
        self.style_prefix = ""

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

    def dim(self):
        self.style_prefix = Term.DIM

    def bold(self):
        self.style_prefix = Term.BOLD

    def reset_color(self):
        self.color_prefix = ""

    def reset_style(self):
        self.style_prefix = ""

    def print(self, text: str, *, end=""):
        print(
                f"{self.prefix}{self.color_prefix}{self.style_prefix}"
                f"{text}{Term.RESET}",
                end=end
        )
        self.reset_style
        self.reset_color()

    def println(self, text: str):
        self.print(text, end=None)

    def ok(self, reason: str, value: str | None):
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

    RESET = "\033[0m"

    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    GOLD = "\033[38;5;220m"

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
