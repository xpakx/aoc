import re
from dataclasses import fields, is_dataclass


def build_regex_pattern(template, repl):
    # Build regex from template
    regex_parts = []
    cursor = 0
    for m in re.finditer(r"{([\w.]+)}", template):
        regex_parts.append(re.escape(template[cursor:m.start()]))
        regex_parts.append(repl(m))
        cursor = m.end()
    regex_parts.append(re.escape(template[cursor:]))

    pattern = "".join(regex_parts)

    pattern = pattern\
        .replace(r"\,", r"\s*,\s*")\
        .replace(r"\@", r"\s*@\s*")\
        .replace(r"\ ", r"\s+")
    return pattern


def get_repl_func(group_map, dtcls_fields):
    def repl(match):
        name = match.group(1)
        safe = name.replace('.', '__')
        group_map[safe] = name
        # TODO: nested fields
        tp = dtcls_fields.get(safe)
        if tp == int or tp == float:
            return f"(?P<{safe}>[-+]?\\d+(?:\\.\\d+)?)"
        else:
            return f"(?P<{safe}>.+?)"
    return repl


def sanitize_field_names(datacls):
    dtcls_fields = {}
    for f in fields(datacls):
        safe = f.name.replace('.', '__')
        dtcls_fields[safe] = f.type
    return dtcls_fields


def prepare_source(text: str | list[str]):
    if type(text) is str:
        return [line.strip() for line in text.strip().splitlines() if line.strip()]
    return text


def parse(
        datacls, template: str,
        text: str | list[str],
        list_separator=" ",
):
    group_map = {}
    dtcls_fields = sanitize_field_names(datacls)

    repl = get_repl_func(group_map, dtcls_fields)
    pattern = build_regex_pattern(template, repl)
    regex = re.compile(r"^" + pattern + r"$")

    lines = prepare_source(text)
    parsed = []

    for line in lines:
        m = regex.match(line)
        if not m:
            print("No match:", line)
            continue

        flat = {}
        for safe, value in m.groupdict().items():
            orig = group_map[safe]
            flat[orig] = value

        nested = {}
        for key, value in flat.items():
            parts = key.split(".")
            cur = nested
            for p in parts[:-1]:
                cur = cur.setdefault(p, {})
            cur[parts[-1]] = value

        def build_instance(cls, values):
            kwargs = {}
            for f in fields(cls):
                if f.name not in values:
                    continue
                v = values[f.name]
                if is_dataclass(f.type):
                    kwargs[f.name] = build_instance(f.type, v)
                elif list_separator and f.type == list[str] or f.type == list[int]:
                    items = v.split(list_separator)
                    if f.type == list[int]:
                        items = list(map(lambda i: int(i), items))
                    kwargs[f.name] = items
                else:
                    try:
                        kwargs[f.name] = f.type(v)
                    except Exception:
                        kwargs[f.name] = v
            return cls(**kwargs)

        parsed.append(build_instance(datacls, nested))

    return parsed
