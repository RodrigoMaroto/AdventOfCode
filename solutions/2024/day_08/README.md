# Day 8 (2024)

`Resonant Collinearity` ([prompt](https://adventofcode.com/2024/day/8))

Yet another grid although I found it to be quite straightforward!

## Part 1
Today, we'll handle the input using the same `Grid` class as explained in [Day 6](../day_06/README.md). In this problem, we have different types of antennas, each represented by a distinct character. These antennas do not interact with each other, allowing us to treat each type as a separate subproblem. Our solution will look like this:

```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        grid = parse_grid(self.input)
        antenna_types = set(grid.values()) - {"."}
        antinodes = set()
        for antenna in antenna_types:
            antinodes.update(find_antinodes(grid, antenna))
        return len(antinodes)
```
The problem today is to count the number of locations where **antinodes** are present. To remove duplicates we use a `set` to store them. according to the instructions, *an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other*.  

In other words, for any pair of antennas, there are two possible antinodes. These can be calculated by finding the vector between the antennas and applying it to each point. This is what we do in the `find_antinodes` function, while also checking that the locations are within the grid.

```py
def find_antinodes(grid: Grid, antenna_type: str) -> set[GridPoint]:
    antennas = [key for key, val in grid.items() if val == antenna_type]
    antinodes = set()
    for i in range(len(antennas)):
        for j in range(i+1, len(antennas)):
            a1, a2 = antennas[i], antennas[j]
            vector = (a1[0] - a2[0], a1[1] - a2[1])         
            if (antinode1 := (a1[0] + vector[0], a1[1] + vector[1])) in grid:
                antinodes.add(antinode1)
            if (antinode2 := (a2[0] - vector[0], a2[1] - vector[1])) in grid:
                antinodes.add(antinode2)
    return antinodes
```

## Part 2
For this second part, the criteria for antinode appearance change slightly. Now, the same vector can be repeated *ad infinitum*, and will include the antennas themselves. To handle these changes while maintaining compatibility with Part 1, we update the `find_antinodes` function. This implementation introduces a mechanism to repeatedly extend the vector, adding new antinode locations as long as they remain within the grid.
```py
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
                ...
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
```
Finally we combine both solutions and it ends up looking like this:
```py
def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        antenna_types = set(grid.values()) - {"."}
        antinodes1 = set()
        antinodes2 = set()
        for antenna in antenna_types:
            antinodes1.update(find_antinodes(grid, antenna, part1=True))
            antinodes2.update(find_antinodes(grid, antenna))

        return len(antinodes1), len(antinodes2)
```