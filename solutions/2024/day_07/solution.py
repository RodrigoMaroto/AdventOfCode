# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/7

from ...base import StrSplitSolution, answer


def valid_equation(result: int, operands: list[int], check_concat: bool = True) -> bool:
    if len(operands) == 1:
        return operands[0] == result

    last = operands[-1]

    if result % last == 0:
        possible_mul = valid_equation(result // last, operands[:-1], check_concat)
    else:
        possible_mul = False

    possible_add = valid_equation(result - last, operands[:-1], check_concat)

    possible_concat = False
    if check_concat:
        shift = 10 ** len(str(last))
        if (result - last) % shift == 0:
            possible_concat = valid_equation((result - last) // shift, operands[:-1])

    return possible_mul or possible_add or possible_concat


class Solution(StrSplitSolution):
    _year = 2024
    _day = 7

    @answer(303766880536)
    def part_1(self) -> int:
        sol = 0
        for line in self.input:
            result, operands = line.split(": ")
            result = int(result)
            operands = [int(x) for x in operands.split(" ")]
            if valid_equation(result, operands, False):
                sol += result
        return sol

    @answer(337041851384440)
    def part_2(self) -> int:
        sol = 0
        for line in self.input:
            result, operands = line.split(": ")
            result = int(result)
            operands = [int(x) for x in operands.split(" ")]
            if valid_equation(result, operands):
                sol += result
        return sol
