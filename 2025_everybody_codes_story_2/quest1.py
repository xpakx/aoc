from utils.loader import get_file_instr
from utils.runner import AdventDay
import heapq


def load(filename) -> tuple[list[str], list[list[int]]]:
    [board, instr] = get_file_instr(filename, split_first_by='\n', split_second_by='\n')
    instr = [[1 if c == 'R' else -1 for c in row] for row in instr]
    return board, instr


def process(start: tuple[int, int], board: list[str], instr: list[int]) -> int:
    pos = start
    i = 0
    while pos[0] < len(board):
        x, y = pos
        symbol = board[x][y]
        if symbol == '*':
            y += instr[i]
            if y < 0:
                y += 2
            elif y >= len(board[x]):
                y -= 2
            i += 1
        pos = (x+1, y)
    return pos[1]


def drop(i: int, board: list[str], instr: list[int]) -> int:
    start = (0, 2*i)
    end = process(start, board, instr)

    start = i + 1
    end = end // 2 + 1
    coins = max(0, (end * 2) - start)
    # print('   ', start, end, coins)
    return coins


def task1(board: list[str], instructions: list[list[int]]):
    coins = 0
    for i, instr in enumerate(instructions):
        coins += drop(i, board, instr)
    return coins


def task2(board: list[str], instructions: list[list[int]]):
    coins = 0
    for instr in instructions:
        max_coins = 0
        for i in range((len(board[0])+1)//2):
            curr_coins = drop(i, board, instr)
            # print("   ", i+1, curr_coins)
            if curr_coins > max_coins:
                max_coins = curr_coins
        coins += max_coins
    return coins


def finished(values: dict[tuple[int, int], int], state: tuple[int]):
    seen = 0
    for i in range(6):
        if state[i] == 0:
            return False
        mask = 1 << state[i]-1
        if seen & mask != 0:
            return False
        seen |= mask
    return True


def find_min(values: dict[tuple[int, int], int], slots_len: int):
    state = tuple([0] * 6)
    queue = [(0, state)]
    visited = set()
    visited.add(state)
    while queue:
        coins, state = heapq.heappop(queue)
        if finished(values, state):
            return coins
        for i in range(6):
            next_state = tuple([x if j != i else x+1 for j, x in enumerate(state)])
            if next_state[i] > slots_len:
                continue
            old = values.get((state[i], i), 0)
            new = values.get((next_state[i], i), 0)
            next_coins = coins - old + new
            if next_state in visited:
                continue
            visited.add(next_state)
            heapq.heappush(queue, (next_coins, next_state))
    assert False


def task3(board: list[str], instructions: list[list[int]]):
    values = {}  # (insert_slot, instruction) -> coins
    slots = (len(board[0])+1) // 2
    for slot in range(slots):
        for instr_id, instr in enumerate(instructions):
            values[(slot+1, instr_id)] = drop(slot, board, instr)
    print(slots)
    print(values)
    return find_min(values, slots)


app = AdventDay()
app.run()
