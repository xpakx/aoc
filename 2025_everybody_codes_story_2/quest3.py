from utils.loader import get_file
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


def load(filename) -> list[Dice]:
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


app = AdventDay()
app.run()
