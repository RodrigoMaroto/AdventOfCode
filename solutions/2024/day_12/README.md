# Day 12 (2024)

`Garden Groups` ([prompt](https://adventofcode.com/2024/day/12))

## Part 1
Another Grid classic where we will use the same parsing technique as explained in [Day 6](../day_06/README.md). Additionally I added a smal helper function to add coordinates.

In this puzzle it was necessary to divide the Grid into regions. Each region was a connected set of coordinates with the same value. I used DFS to find those regions as you can see in this code. Once `plotRegion` is called it will return a set that contains all the coordinates of said region. Additionally, i will store in a global variable the locations already visited. In the main segment, for each location not already included in a region, it will call the mentioned function.
```py
def plotRegion(
    region: set[GridPoint], grid: Grid, location: GridPoint
) -> set[GridPoint]:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    region.add(location)
    visited.add(location)
    for d in directions:
        new_loc = add_points(location, d)
        if (
            new_loc in grid
            and grid[location] == grid[new_loc]
            and new_loc not in region
        ):
            plotRegion(region, grid, new_loc)
    return region

class Solution(StrSplitSolution):
    def part_1(self) -> int:
        grid = parse_grid(self.input)
        regions = [plotRegion(set(), grid, pos) for pos in grid if pos not in visited]
```
To find the solution we need to add the cost of each region. This is calculated by multiplying the area by the perimeter. The area is easy to find as each location equals `1` unit. To find the perimeter we will use a function that will iterate through each location in a region and count how many sides are not neighbouring another plot of the same region.

```py
def perimeter(region: set[GridPoint]) -> int:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    res = 0
    for plot in region:
        for d in directions:
            if add_points(plot, d) not in region:
                res += 1
    return res

class Solution(StrSplitSolution):
    def part_1(self) -> int:
        ...
        return sum(len(r) * perimeter(r) for r in regions)
```

## Part 2
For the second part, instead of the perimeter, we need to count the number of sides that the region has. A nice trick that makes solving it much easier is that counting sides is exactly the same as counting corners. Therefore, in a new helper function we check if it does not have a region neighbour on two sides, which would be an outer corner, or if it has both and the corresponding diagonal is different.
```py
def sides(region: set[GridPoint]) -> int:
    out_corners = [
        [(-1, 0), (0, -1)],
        [(-1, 0), (0, 1)],
        [(1, 0), (0, -1)],
        [(1, 0), (0, 1)],
    ]
    res = 0
    for plot in region:
        for c in out_corners:
            if all(add_points(plot, d) not in region for d in c) or (
                all(add_points(plot, d) in region for d in c)
                and add_points(plot, add_points(c[0], c[1])) not in region
            ):
                res += 1
    return res
```

Finally we put both parts together to obtain the solution for Day 12!
```py
class Solution(StrSplitSolution):
    def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        regions = [plotRegion(set(), grid, pos) for pos in grid if pos not in visited]
        part1 = sum(len(r) * perimeter(r) for r in regions)
        part2 = sum(len(r) * sides(r) for r in regions)
        return part1, part2
```
