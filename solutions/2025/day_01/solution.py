# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/1

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2025
    _day = 1

    @answer(1029)
    def part_1(self) -> int:
        result = 0
        pos = 50
        for line in self.input:
            direction, distance = line[0], int(line[1:])
            pos += distance if direction == "R" else -distance
            pos %= 100
            result += 1 if pos == 0 else 0
        return result

    @answer(5892)
    def part_2(self) -> int:
        result = 0
        pos = 50
        for line in self.input:
            direction, distance = line[0], int(line[1:])
            old_pos = pos
            pos += distance if direction == "R" else -distance

            turns, pos = divmod(pos, 100)
            result += abs(turns)

            ## Edge cases on turning left
            if direction == "L" and pos == 0:
                result += 1
            if direction == "L" and old_pos == 0:
                result -= 1

        return result

    @answer((1029, 5892))
    def solve(self) -> tuple[int, int]:
        result1 = 0
        result2 = 0
        pos = 50
        for line in self.input:
            direction, distance = line[0], int(line[1:])
            old_pos = pos
            pos += distance if direction == "R" else -distance

            turns, pos = divmod(pos, 100)
            result1 += 1 if pos == 0 else 0
            result2 += abs(turns)

            ## Edge cases on turning left
            if direction == "L" and pos == 0:
                result2 += 1
            if direction == "L" and old_pos == 0:
                result2 -= 1

        return result1, result2 
