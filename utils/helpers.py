def clamp(n, smallest, largest):
    if n < smallest:
        return smallest
    if n > largest:
        return largest
    return n


def transform_steps(steps, lval=-1, rval=1):
    return list(
            map(
                lambda inst: [
                    (lval if inst[0] == 'L' else rval),
                    int(inst[1:])
                    ],
                steps
                )
            )


def swap(lst, i1, i2):
    n = lst[i1]
    lst[i1] = lst[i2]
    lst[i2] = n
