class Term:
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

