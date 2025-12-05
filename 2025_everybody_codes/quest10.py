from utils.loader import get_map
from utils.runner import AdventDay
from enum import Enum


class Tile(Enum):
    empty = 0
    sheep = 1
    dragon = 2
    wall = 3


def load(filename):
    map = get_map(filename, Tile,
                  dct={
                      'S': Tile.sheep,
                      'D': Tile.dragon,
                      '#': Tile.wall,
                      }
                  )
    dragon_row = next(
            filter(lambda x: Tile.dragon in x[1], enumerate(map))
    )
    dragon_tile = next(
            filter(lambda x: Tile.dragon == x[1], enumerate(dragon_row[1]))
    )
    return map, [dragon_row[0], dragon_tile[0]]


moves = [
        [2, 1], [2, -1], [-2, 1], [-2, -1],
        [1, 2], [1, -2], [-1, 2], [-1, -2]
]


def part1(map, dragon_pos):
    stack = [[*dragon_pos, 0]]
    visited = [[-1 for tile in row] for row in map]
    result = 0
    max_steps = 4
    while len(stack) > 0:
        [i, j, steps] = stack.pop()
        if steps > max_steps:
            continue
        vis = visited[i][j]
        if vis > 0 and vis <= steps:
            continue
        if vis > steps:
            visited[i][j] = steps
        for m in moves:
            new_i = i + m[0]
            new_j = j + m[1]
            if new_i < 0 or new_j < 0:
                continue
            if new_i >= len(map) or new_j >= len(map[new_i]):
                continue
            stack.append([new_i, new_j, steps+1])
        if visited[i][j] > 0:
            continue
        visited[i][j] = steps
        if map[i][j] == Tile.sheep:
            result += 1
    return result


def part2(map, dragon_pos):
    stack = [[*dragon_pos, 0]]
    max_steps = 20
    visited = [[[False for tile in row] for row in map] for step in range(max_steps+1)]
    result = 0
    while len(stack) > 0:
        [i, j, steps] = stack.pop()
        if steps > max_steps:
            continue
        vis = visited[steps][i][j]
        if vis:
            continue
        for m in moves:
            new_i = i + m[0]
            new_j = j + m[1]
            if new_i < 0 or new_j < 0:
                continue
            if new_i >= len(map) or new_j >= len(map[new_i]):
                continue
            stack.append([new_i, new_j, steps+1])
        visited[steps][i][j] = True

        sheep_i = i - steps
        if sheep_i >= 0 and map[sheep_i][j] == Tile.sheep and not map[i][j] == Tile.wall:
            map[sheep_i][j] = Tile.empty
            result += 1
        if steps == 0:
            continue

        sheep_i = i - steps + 1
        if sheep_i >= 0 and map[sheep_i][j] == Tile.sheep and not map[i][j] == Tile.wall:
            map[sheep_i][j] = Tile.empty
            result += 1

    return result


class BitBoard:
    def __init__(self, map):
        self.sheeps = 0
        self.walls = 0
        self.dragon = 0
        self.width = len(map[0])
        self.height = len(map)
        self.size = self.width * self.height
        self.board_mask = 0
        for row in map:
            for tile in row:
                self.board_mask <<= 1
                self.board_mask += 1
                self.sheeps <<= 1
                if tile == Tile.sheep:
                    self.sheeps += 1
                self.walls <<= 1
                if tile == Tile.wall:
                    self.walls += 1
                self.dragon <<= 1
                if tile == Tile.dragon:
                    self.dragon += 1

            self.gen_dragon_lookup()
            self.last_rank_mask = (1 << self.width) - 1

    def gen_dragon_lookup(self):
        self.dragon_lookup = []

        for i in range(self.size):
            r = i // self.width
            c = i % self.width

            mask = 0
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    target_idx = nr * self.width + nc
                    mask |= (1 << (self.size - 1 - target_idx))
            self.dragon_lookup.append(mask)

    def gen_sheep_moves(self):
        return (self.sheeps >> self.width) & self.board_mask & ~(self.dragon & ~self.walls)

    def gen_sheep_promotions(self):
        return self.sheeps & self.last_rank_mask

    def get_vulnerable_sheep(self):
        return self.sheeps & ~self.walls

    def gen_dragon_moves(self):
        dragon_index = self.size - self.dragon.bit_length()
        return self.dragon_lookup[dragon_index]

    def move_dragon(self, mask):
        self.dragon = self.dragon ^ mask

    def move_sheep(self, mask):
        self.sheeps = self.sheeps ^ mask

    def print(self):
        sheep = self.sheeps
        dragon = self.dragon
        walls = self.walls
        for i in range(self.height):
            for j in range(self.width):
                index = (self.height-i-1)*self.width + j
                if sheep >> index & 1 > 0:
                    print("S", end="")
                elif dragon >> index & 1 > 0:
                    print("D", end="")
                elif walls >> index & 1 > 0:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def to_algebraic(self, move_mask):
        if move_mask == 0:
            return "None"
        idx = self.size - move_mask.bit_length()
        row = self.width - (idx // self.width)
        col = idx % self.width
        file_char = chr(ord('A') + col)
        rank_num = self.height - row
        return f"{file_char}{rank_num}"


def print_bin(num):
    print(''.join(reversed(format(num, '#014b')[2:])))


def sheep_move(board, mem):
    key = (board.dragon, board.sheeps, 0)
    if key in mem:
        return mem[key]
    mem[key] = 0
    moves = board.gen_sheep_moves()
    wins = 0
    if moves == 0:
        promotions = board.gen_sheep_promotions()
        if promotions > 0:
            return 0
        wins += dragon_move(board, mem)

    while moves:
        move = moves & (~moves+1)
        move_map = move ^ (move << board.width)
        board.move_sheep(move_map)
        wins += dragon_move(board, mem)
        board.move_sheep(move_map)
        moves ^= move
    mem[key] = wins
    return wins


def dragon_move(board, mem):
    key = (board.dragon, board.sheeps, 1)
    if key in mem:
        return mem[key]
    mem[key] = 0
    moves = board.gen_dragon_moves()
    wins = 0
    while moves:
        move = moves & (~moves+1)
        move_mask = move ^ board.dragon
        board.move_dragon(move_mask)
        capture = board.dragon & board.get_vulnerable_sheep()
        board.move_sheep(capture)
        if board.sheeps.bit_count() == 0:
            wins += 1
        else:
            wins += sheep_move(board, mem)
        board.move_sheep(capture)
        board.move_dragon(move_mask)
        moves ^= move
    mem[key] = wins
    return wins


def part3(map, pos):
    board = BitBoard(map)
    result = sheep_move(board, {})
    return result


app = AdventDay()
app.run()
