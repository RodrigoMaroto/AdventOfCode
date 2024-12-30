# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/22

from collections import defaultdict
from itertools import pairwise

from ...base import IntSplitSolution, answer, slow


def secret_num(n: int) -> int:
    n = (n ^ (n << 6)) & 0xFFFFFF
    n = (n ^ (n >> 5)) & 0xFFFFFF
    return (n ^ (n << 11)) & 0xFFFFFF


class Solution(IntSplitSolution):
    _year = 2024
    _day = 22

    # @answer(16953639210)
    def part_1(self) -> int:
        result = 0
        for i in self.input:
            res = i
            for _ in range(2000):
                res = secret_num(res)
            result += res
        return result

    # @answer(1234)
    def part_2(self) -> int:
        result = defaultdict(int)
        for i in self.input:
            nums = [i] + [i := secret_num(i) for _ in range(2000)]
            diffs = [(b % 10) - (a % 10) for a, b in pairwise(nums)]
            seen = set()
            for i in range(len(nums) - 4):
                pat = tuple(diffs[i : i + 4])
                if pat not in seen:
                    result[pat] += nums[i + 4] % 10
                    seen.add(pat)
        return max(result.values())

    @slow
    @answer((16953639210, 1863))
    def solve(self) -> tuple[int, int]:
        part1 = 0
        patterns = defaultdict(int)
        for i in self.input:
            nums = [i] + [i := secret_num(i) for _ in range(2000)]
            part1 += nums[-1]
            diffs = [(b % 10) - (a % 10) for a, b in pairwise(nums)]
            seen = set()
            for i in range(len(nums) - 4):
                pat = tuple(diffs[i : i + 4])
                if pat not in seen:
                    patterns[pat] += nums[i + 4] % 10
                    seen.add(pat)
        return part1, max(patterns.values())
