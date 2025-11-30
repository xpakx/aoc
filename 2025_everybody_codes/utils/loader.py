def get_file(path, *, split_lines=True, split_by=None, strip=True, as_int=False):
    if split_by is not None:
        split_lines = False
    if path is None:
        raise ValueError("Requires a file path")

    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    if split_lines:
        data = data.splitlines()
        if strip:
            data = [line.strip() for line in data]
        if as_int:
            data = [int(x) for x in data if x]
    elif split_by:
        data = data.split(split_by)
        if strip:
            data = [line.strip() for line in data]
        if as_int:
            data = [int(x) for x in data if x]
    elif strip:
        data = data.strip()
    return data


def get_file_single(path, *, strip=True, as_int=False): 
    return get_file(
            path, split_lines=False, strip=strip, as_int=as_int
    )


def get_file_instr(path, *, strip=True, as_int=False,
                   split_first_by=',', split_second_by=','):
    [a, b] = get_file(
            path, split_lines=False, split_by='\n\n',
            strip=strip, as_int=as_int
    )
    if not split_first_by and not split_second_by:
        return [a, b]
    if split_first_by:
        a = a.split(split_first_by)
    if split_second_by:
        b = b.split(split_second_by)
    return [a, b]
