# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/14

import math
import re
from statistics import variance

from ...base import StrSplitSolution, answer


def simulate(
    t: int, width: int, height: int, robots: list[list[int]]
) -> list[tuple[int, int]]:
    return [
        ((sx + t * vx) % width, (sy + t * vy) % height) for (sx, sy, vx, vy) in robots
    ]


class Solution(StrSplitSolution):
    _year = 2024
    _day = 14

    @answer(224969976)
    def part_1(self) -> int:
        data = [[int(i) for i in re.findall(r"-?\d+", s)] for s in self.input]
        cuadrants = [0 for _ in range(4)]
        width = 101
        height = 103
        for i in data:
            x = (i[0] + i[2] * 100) % width
            y = (i[1] + i[3] * 100) % height
            if x < width // 2:
                if y < height // 2:
                    cuadrants[0] += 1
                elif y > height // 2:
                    cuadrants[2] += 1
            elif x > width // 2:
                if y < height // 2:
                    cuadrants[1] += 1
                elif y > height // 2:
                    cuadrants[3] += 1
        return math.prod(cuadrants)

    @answer(7892)
    def part_2(self) -> int:
        data = [[int(i) for i in re.findall(r"-?\d+", s)] for s in self.input]
        width = 101
        height = 103
        bx, bxvar, by, byvar = 0, 10 * 100, 0, 10 * 1000
        for t in range(max(width, height)):
            xs, ys = zip(*simulate(t, width, height, data))
            if (xvar := variance(xs)) < bxvar:
                bx, bxvar = t, xvar
            if (yvar := variance(ys)) < byvar:
                by, byvar = t, yvar
        return bx + ((pow(width, -1, height) * (by - bx)) % height) * width
