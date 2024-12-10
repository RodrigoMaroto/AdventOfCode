# Day 10 (2024)

`Hoof It` ([prompt](https://adventofcode.com/2024/day/10))

Topographic map search where I managed to basically do Part 2 while doing Part 1.

## Part 1
Today, we'll handle the input using the same `Grid` class as explained in [Day 6](../day_06/README.md). In addition to that, I created a helper function to obtain all the existing neighbouring locations excluding diagonals.
```py
def get_neighbours(grid: Grid, location: GridPoint) -> tuple[GridPoint]:
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    return tuple(
        loc
        for v in directions
        if (loc := (location[0] + v[0], location[1] + v[1])) in grid
    )
```
To solve this problem, I created a `search` function that implements a DFS recursively and returns the mountain tops (represented with a `9`) reached from any starting position. By returning a list instead of a set, this will include duplicate locations. If any location appears n times, it means there are n paths to reach it.

```py
def search(grid: Grid, location: GridPoint, prev_height: int) -> list[GridPoint]:
    height = grid[location]
    if height != prev_height + 1:
        return []
    if height == 9:
        return [location]
    locations = []
    for n in get_neighbours(grid, location):
        locations += search(grid, n, height)
    return locations
```
We can easily add the distinct mountain tops reachable from each trailhead (represented with a `0`) and return the solution:
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        grid = parse_grid(self.input)
        trailheads = [loc for loc in grid if grid[loc] == 0]
        return sum(len(set(search(grid, start, -1))) for start in trailheads)
```

## Part 2
For this second part, we need to count the number of different trails that originate from each trailhead. As I explained before, the `search` function already gives that information. So we can easily combine those two parts creating a very efficient solution for both:
```py
class Solution(StrSplitSolution):
    def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        trailheads = [loc for loc in grid if grid[loc] == 0]
        reached_tops = [search(grid, start, -1) for start in trailheads]
        part1 = sum(len(set(x)) for x in reached_tops)
        part2 = sum(len(x) for x in reached_tops)
        return part1, part2
```
