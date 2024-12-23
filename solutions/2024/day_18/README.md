# Day 18 (2024)

`RAM Run` ([prompt](https://adventofcode.com/2024/day/18))


## Part 1
Another 2D puzzle, but today I modified the `parse_grid` function to just return am empty (`.`) 71x71 grid where obstacles will later be placed at the coordinates given in the input. 

```py
def parse_grid() -> Grid:
    result = {}
    for row in range(71):
        for col in range(71):
            result[row, col] = "."
    return result
```
As I said before the obstacles are added sequentially in the coordinates provided in the input. In this `run` function, we simply create a grid with the number of obstacles we determine with the `iterations` argument and then we run our dijkstra function.
```py
def run(iterations: int, obstacles: list[str]) -> int:
    grid = parse_grid()
    for i in range(iterations):
        point = GridPoint(map(int, obstacles[i].split(",")))
        grid[point] = "#"
    return dijkstra(grid, (0, 0), (70, 70))
```
In order to find the length of the shortest path from the start `(0,0)` to the end `(70,70)`, we use the Dijkstra Algorithm that we also applied in [Day 16](../day_16/README.md). This will give us the minimum distance and `-1` in case there is no answer, meaning that there are too many obstacles that make it impossible to find a path.
```py
def dijkstra(grid: Grid, start: GridPoint, end: GridPoint) -> int:
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    open_set = [(0, start)]
    closed_set = {start}

    while open_set:
        score, target = open_set.pop(0)

        if target == end:
            return score

        for d in dirs:
            ntarget = add_points(target, d)
            if ntarget not in closed_set and ntarget in grid and grid[ntarget] != "#":
                open_set.append((score + 1, ntarget))
                closed_set.add(ntarget)
    return -1
```
To obtain the solution for this we just need to execute the `run` function adding `1024` obstacles.

## Part 2
In Part 2, we need to find the coordinates of the obstacle that makes the maze unsolvable, which as I said before will make our output `-1`. To make this more efficient, I implemented a Binary Search, which reduces the complexity from linear to logarithmic.

```py
class Solution(StrSplitSolution):
    def part_2(self) -> str:
        low = 0
        high = len(self.input)
        while high - low > 1:
            avg = (low + high) // 2
            if run(avg, self.input) == -1:
                high = avg
            else:
                low = avg
        return self.input[low]
```
