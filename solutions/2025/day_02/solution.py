# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/2

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2025
    _day = 2
    StrSplitSolution.separator = ","

    # @answer(40214376723)
    def part_1(self) -> int:
        result = 0
        for line in self.input:
            for id in range(int(line.split("-")[0]), int(line.split("-")[1]) + 1):
                id_str = str(id)
                l = len(id_str)
                if l % 2 == 0 and id_str[:l//2] == id_str[l//2:]:
                    result += id
        return result
            

    # @answer(50793864718)
    def part_2(self) -> int:
        result = 0
        for line in self.input:
            for id in range(int(line.split("-")[0]), int(line.split("-")[1]) + 1):
                id_str = str(id)
                l = len(id_str)
                for i in range(1, l):
                    if l % i == 0:
                        if all(id_str[j:i + j] == id_str[0:i] for j in range(i, l, i)):
                            result += id
                            break
        return result

    @answer((40214376723, 50793864718))
    def solve(self) -> tuple[int, int]:
        result1 = 0
        result2 = 0
        for line in self.input:
            for id in range(int(line.split("-")[0]), int(line.split("-")[1]) + 1):
                id_str = str(id)
                l = len(id_str)
                if l % 2 == 0 and id_str[:l//2] == id_str[l//2:]:
                    result1 += id
                for i in range(1, l):
                    if l % i == 0:
                        if all(id_str[j:i + j] == id_str[0:i] for j in range(i, l, i)):
                            result2 += id
                            break
        return result1, result2
