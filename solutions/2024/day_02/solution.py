# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/2

from ...base import StrSplitSolution, answer


def is_sorted(report: list[int]) -> bool:
    if report[1] >= report[0]:  # increasing
        return all(report[i] <= report[i + 1] for i in range(len(report) - 1))
    # decreasing
    return all(report[i] >= report[i + 1] for i in range(len(report) - 1))


def safe_report(report: list[int]) -> bool:
    if not is_sorted(report):
        return False
    for i in range(len(report) - 1):
        diff = abs(report[i] - report[i + 1])
        if not 1 <= diff <= 3:
            return False
    return True


def safe_report2(report: list[int]) -> bool:
    if safe_report(report):
        return True
    for i in range(len(report)):
        report_cp = report.copy()
        report_cp.pop(i)
        if safe_report(report_cp):
            return True
    return False


class Solution(StrSplitSolution):
    _year = 2024
    _day = 2

    @answer(299)
    def part_1(self) -> int:
        reports = [list(map(int, line.split())) for line in self.input]
        return sum([safe_report(report) for report in reports])

    @answer(364)
    def part_2(self) -> int:
        reports = [list(map(int, line.split())) for line in self.input]
        return sum([safe_report2(report) for report in reports])

    @answer((299, 364))
    def solve(self) -> tuple[int, int]:
        reports = [list(map(int, line.split())) for line in self.input]
        part1 = sum([safe_report(report) for report in reports])
        part2 = sum([safe_report2(report) for report in reports])
        return part1, part2
