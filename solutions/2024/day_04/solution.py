# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/4

from ...base import StrSplitSolution, answer


def check_xmas(matrix: list[list[str]], x: int, y: int) -> int:
    if matrix[y][x] != "X":
        return 0
    valid_count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (
                matrix[y + i][x + j] == "M"
                and matrix[y + i * 2][x + j * 2] == "A"
                and matrix[y + i * 3][x + j * 3] == "S"
            ):
                valid_count += 1
    return valid_count


def check_x_mas(matrix: list[list[str]], x: int, y: int) -> bool:
    if matrix[y][x] != "A":
        return False
    return {matrix[y + 1][x + 1], matrix[y - 1][x - 1]} == {"M", "S"} and {
        matrix[y + 1][x - 1],
        matrix[y - 1][x + 1],
    } == {"M", "S"}


class Solution(StrSplitSolution):
    _year = 2024
    _day = 4

    @answer(2464)
    def part_1(self) -> int:
        matrix = [["."] + list(line) + ["."] for line in self.input]
        matrix.insert(0, ["."] * len(matrix[0]))
        matrix.append(["."] * len(matrix[0]))
        return sum(
            check_xmas(matrix, x, y)
            for y in range(len(matrix))
            for x in range(len(matrix[0]))
        )

    @answer(1982)
    def part_2(self) -> int:
        matrix = [["."] + list(line) + ["."] for line in self.input]
        matrix.insert(0, ["."] * len(matrix[0]))
        matrix.append(["."] * len(matrix[0]))
        return sum(
            check_x_mas(matrix, x, y)
            for y in range(len(matrix))
            for x in range(len(matrix[0]))
        )

    @answer((2464, 1982))
    def solve(self) -> tuple[int, int]:
        matrix = [["."] + list(line) + ["."] for line in self.input]
        matrix.insert(0, ["."] * len(matrix[0]))
        matrix.append(["."] * len(matrix[0]))
        part1 = sum(
            check_xmas(matrix, x, y)
            for y in range(len(matrix))
            for x in range(len(matrix[0]))
        )
        part2 = sum(
            check_x_mas(matrix, x, y)
            for y in range(len(matrix))
            for x in range(len(matrix[0]))
        )
        return part1, part2
