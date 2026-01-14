from utils.loader import get_file, get_file_instr
from utils.parser import parse
from utils.runner import AdventDay
from dataclasses import dataclass


@dataclass
class Dice:
    id: int
    faces: list[int]
    seed: int
    rolled: int = 0
    pulse: int = 0

    def reset(self):
        self.pulse = self.seed

    def result(self) -> int:
        return self.faces[self.rolled]

    def roll(self, roll_number: int) -> int:
        spin = roll_number * self.pulse
        self.rolled = (self.rolled + spin) % len(self.faces)
        return self.result()

    def update_pulse(self, roll_number: int) -> int:
        spin = roll_number * self.pulse
        self.pulse += spin
        self.pulse = self.pulse % self.seed
        self.pulse = self.pulse + 1 + roll_number + self.seed
        return self.pulse


def load1(filename) -> list[Dice]:
    data = get_file(filename)
    return parse(Dice, "{id}: faces=[{faces}] seed={seed}", data,
                 list_separator=',')


def task1(dices: list[Dice]) -> int:
    sum = 0
    for dice in dices:
        dice.reset()
    roll_number = 0
    while sum <= 10000:
        roll_number += 1
        for dice in dices:
            # print("Dice", dice.id)
            result = dice.roll(roll_number)
            # print(result)
            sum += result
            dice.update_pulse(roll_number)
    print(dices)
    return roll_number


def load(filename) -> tuple[list[Dice], list[int]]:
    data, instr = get_file_instr(filename, split_first_by='\n')
    dices = parse(Dice, "{id}: faces=[{faces}] seed={seed}", data,
                  list_separator=',')
    return dices, [int(x) for x in list(instr[0])]


class Player:
    def __init__(self, dice: Dice, track: list[int]):
        self.dice = dice
        dice.reset()
        self.position = 0
        self.finished = False
        self.finished_at = 0
        self.track = track

    def move(self, roll_number: int) -> bool:
        current = self.track[self.position]
        result = self.dice.roll(roll_number)
        self.dice.update_pulse(roll_number)
        if result == current:
            self.position += 1
            self.finished = self.position >= len(self.track)
        if self.finished:
            self.finished_at = roll_number

        return self.finished


def task2(dices: list[Dice], racetrack: list[int]) -> int:
    print(dices)
    print(racetrack)
    players = [Player(dice, racetrack) for dice in dices]
    roll_number = 0
    while True:
        roll_number += 1
        moved = False
        for player in players:
            if player.finished:
                continue
            moved = True
            player.move(roll_number)
        if not moved:
            break
    result = [(p.finished_at, p.dice.id) for p in players]
    result.sort()
    result = [str(p[1]) for p in result]
    return ','.join(result)


app = AdventDay()
app.run()
