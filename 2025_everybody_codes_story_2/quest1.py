from utils.loader import get_file_instr
from utils.runner import AdventDay
import heapq
import random


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
        mask = 1 << state[i]
        if seen & mask != 0:
            return False
        seen |= mask
    return True


def task3(board: list[str], instructions: list[list[int]]):
    values = {}  # (insert_slot, instruction) -> coins
    slots = (len(board[0])+1) // 2
    for slot in range(slots):
        for instr_id, instr in enumerate(instructions):
            values[(slot, instr_id)] = drop(slot, board, instr)
    print(slots)
    print(values)

    dp_min = [1 << 31] * (1 << slots)
    dp_max = [0] * (1 << slots)
    dp_min[0] = dp_max[0] = 0
    to_check = {0}
    for i, instr in enumerate(instructions):
        to_check_new = set()
        for start_slot in range(slots):
            for pos in to_check:
                pos_new = pos | (1 << start_slot)
                if pos_new != pos:
                    dp_min[pos_new] = min(
                            dp_min[pos_new],
                            dp_min[pos] + values[(start_slot, i)])
                    dp_max[pos_new] = max(
                            dp_max[pos_new],
                            dp_max[pos] + values[(start_slot, i)])
                    to_check_new.add(pos_new)
        to_check = to_check_new

    ans_min = min(dp_min[pos] for pos in to_check)
    ans_max = max(dp_max[pos] for pos in to_check)

    return f'{ans_min} {ans_max}'


app = AdventDay()
app.run()
