# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/1

from collections import Counter

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2024
    _day = 1

    @answer(1388114)
    def part_1(self) -> int:
        left_list, right_list = [], []
        for line in self.input:
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))
        left_list.sort()
        right_list.sort()
        return sum([abs(left_list[i] - right_list[i]) for i in range(len(left_list))])

    @answer(23529853)
    def part_2(self) -> int:
        left_list, right_list = [], []
        for line in self.input:
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))
        right_count = Counter(right_list)
        return sum([right_count[num] * num for num in left_list])
    
    @answer((1388114, 23529853))
    def solve(self):
        left_list, right_list = [], []
        for line in self.input:
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))

        left_list.sort()
        right_list.sort()
        right_count = Counter(right_list)

        total_distance = sum([abs(left_list[i] - right_list[i]) for i in range(len(left_list))])
        similarity_score = sum([right_count[num] * num for num in left_list])
        
        return total_distance, similarity_score
            
