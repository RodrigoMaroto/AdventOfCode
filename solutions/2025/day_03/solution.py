# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/3

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2025
    _day = 3

    # @answer(1234)
    def part_1(self) -> int:
        result = 0
        for bank in self.input:
            joltage = 0
            batteries = [int(x) for x in bank]
            for n in range(9, 0, -1):
                if n in batteries[:-1]:
                    joltage += n * 10
                    break
            batteries = batteries[batteries.index(joltage//10)+1:]
            joltage += max(batteries)
            result += joltage
        return result
            

    # @answer(1234)
    def part_2(self) -> int:
        result = 0
        for bank in self.input:
            joltage = 0
            batteries = [int(x) for x in bank]
            for digit in range(12, 1, -1):
                selected = 0
                for n in range(9, 0, -1):
                    if n in batteries[:-digit + 1]:
                        joltage += n * (10 ** (digit-1))
                        selected = n
                        break
                batteries = batteries[batteries.index(selected)+1:]
            joltage += max(batteries)
            result += joltage
        return result
    
    def calculate_joltage(self, bank: list[int], digits: int) -> int:
        joltage = 0
        batteries = bank.copy()
        for digit in range(digits, 1, -1):
            selected = max(batteries[:-digit + 1])
            joltage += selected * (10 ** (digit-1))
            batteries = batteries[batteries.index(selected)+1:]
        joltage += max(batteries)
        return joltage

    @answer((17324, 171846613143331))
    def solve(self) -> tuple[int, int]:
        result1, result2 = 0, 0
        for line in self.input:
            batteries = [int(x) for x in line]
            result1 += self.calculate_joltage(batteries, 2)
            result2 += self.calculate_joltage(batteries, 12)
        return result1, result2

