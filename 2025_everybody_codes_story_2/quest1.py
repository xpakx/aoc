from utils.loader import get_file_instr
from utils.runner import AdventDay


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


def task1(board: list[str], instructions: list[list[int]]):
    coins = 0
    for i, instr in enumerate(instructions):
        start = (0, 2*i)
        end = process(start, board, instr)

        start = i + 1
        end = end // 2 + 1
        coins += max(0, (end * 2) - start)
        print(start, end, coins)
    print(board)
    print(instructions)
    return coins


app = AdventDay()
app.run()
