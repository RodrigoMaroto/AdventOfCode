# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/8

from ...base import StrSplitSolution, answer

GridPoint = tuple[int, int]
Grid = dict[GridPoint, str]


def find_antinodes(
    grid: Grid, antenna_type: str, part1: bool = False
) -> set[GridPoint]:
    antennas = [key for key, val in grid.items() if val == antenna_type]
    antinodes = set()
    for i in range(len(antennas)):
        for j in range(i + 1, len(antennas)):
            a1, a2 = antennas[i], antennas[j]
            vector = (a1[0] - a2[0], a1[1] - a2[1])
            if part1:
                if (antinode1 := (a1[0] + vector[0], a1[1] + vector[1])) in grid:
                    antinodes.add(antinode1)
                if (antinode2 := (a2[0] - vector[0], a2[1] - vector[1])) in grid:
                    antinodes.add(antinode2)
            else:
                k = 0
                while True:
                    new_node = (a1[0] + k * vector[0], a1[1] + k * vector[1])
                    if new_node not in grid:
                        break
                    antinodes.add(new_node)
                    k += 1
                k = 0
                while True:
                    new_node = (a2[0] - k * vector[0], a2[1] - k * vector[1])
                    if new_node not in grid:
                        break
                    antinodes.add(new_node)
                    k += 1
    return antinodes


def parse_grid(raw_grid: list[str]) -> Grid:
    """
    returns 2-tuples of (row, col) with their value
    """
    result = {}

    for row, line in enumerate(raw_grid):
        for col, c in enumerate(line):
            result[row, col] = c

    return result


class Solution(StrSplitSolution):
    _year = 2024
    _day = 8

    @answer(293)
    def part_1(self) -> int:
        grid = parse_grid(self.input)
        antenna_types = set(grid.values()) - {"."}
        antinodes = set()
        for antenna in antenna_types:
            antinodes.update(find_antinodes(grid, antenna, part1=True))

        return len(antinodes)

    @answer(934)
    def part_2(self) -> int:
        grid = parse_grid(self.input)
        antenna_types = set(grid.values()) - {"."}
        antinodes = set()
        for antenna in antenna_types:
            antinodes.update(find_antinodes(grid, antenna))

        return len(antinodes)

    @answer((293, 934))
    def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        antenna_types = set(grid.values()) - {"."}
        antinodes1 = set()
        antinodes2 = set()
        for antenna in antenna_types:
            antinodes1.update(find_antinodes(grid, antenna, part1=True))
            antinodes2.update(find_antinodes(grid, antenna))

        return len(antinodes1), len(antinodes2)
