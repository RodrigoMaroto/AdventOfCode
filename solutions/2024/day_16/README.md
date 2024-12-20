# Day 16 (2024)

`Reindeer Maze` ([prompt](https://adventofcode.com/2024/day/16))

Today's challenge involves navigating through a grid-based maze using a modified version of Dijkstra's algorithm.

## Part 1
As usual we parse this 2D puzzle using the technique explained in [Day 6](../day_06/README.md). In the first part we need to find the minimum cost from `start` to `end` in this maze. Each step forward will be `1` cost unit and turning in any direction `1000`. To do this in the most efficient way, I decided to use the [Dijkstra Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) that you can see implemented here that will return the cost of the minimum path.

```py
def dijkstra(grid, start, end):
    distances = defaultdict(lambda:(float("inf")))
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]
    distances[start, 1] = 0
    queue = [(0, start, 1)]
    while queue:
        dist, pos, di = heapq.heappop(queue)
        for ndi in range(-1, 2):
            ndir = dirs[(di+ndi)%4]
            npos, ndist = add_points(pos, ndir), dist + 1 + 1000*(ndi!=0)
            if npos == end:
                return ndist
            if grid[npos] != "#":
                o_dist = distances[npos, (di+ndi)%4]
                if o_dist >= ndist:
                    distances[npos, (di+ndi)%4] = ndist
                    heapq.heappush(queue, (ndist, npos, (di+ndi)%4))

class Solution(StrSplitSolution):
    def part1(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        start = list(grid.keys())[list(grid.values()).index("S")]
        end = list(grid.keys())[list(grid.values()).index("E")]
        return dijkstra(grid, start, end)
```

## Part 2
In the second part, we need to calculate the number of distinct segments that are part of any of the possible paths with the minimum cost from `start` to `end`. Since multiple paths may share the same minimum cost but traverse different portions of the grid, we need to track the unique segments visited along these paths.

To adapt Dijkstra’s algorithm for this purpose, we track not only the distances but also the set of segments traversed for each position and direction. This is achieved by maintaining a record of all segments visited in a set `nset`.

```py
def dijkstra(grid: Grid, start: GridPoint, end: GridPoint) -> tuple[int, int]:
    distances = defaultdict(lambda: (float("inf"), set()))
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    distances[start, 1] = (0, set())
    queue = [(0, start, 1)]
    while queue:
        dist, pos, di = heapq.heappop(queue)
        _, p_set = distances[pos, di]
        for ndi in range(-1, 2):
            ndir = dirs[(di + ndi) % 4]
            npos, ndist = add_points(pos, ndir), dist + 1 + 1000 * (ndi != 0)
            while (
                grid[npos] != "#"
                and grid[(npos[0] + ndir[1], npos[1] + ndir[0])] == "#"
                and grid[(npos[0] - ndir[1], npos[1] - ndir[0])] == "#"
            ):
                npos, ndist = add_points(npos, ndir), ndist + 1
            nset = p_set | {seg(pos, npos)}
            if npos == end:
                return ndist, countsegs(nset)
            if grid[npos] != "#":
                o_dist, o_set = distances[npos, (di + ndi) % 4]
                if o_dist == ndist and any((pos not in o_set) for pos in nset):
                    o_set.update(nset)
                    heapq.heappush(queue, (ndist, npos, (di + ndi) % 4))
                if o_dist > ndist:
                    distances[npos, (di + ndi) % 4] = ndist, nset
                    heapq.heappush(queue, (ndist, npos, (di + ndi) % 4))
```

Once we have the set of all segments traversed in the optimal paths, we count the number of unique segments using the helper function `countsegs`. This function calculates the total number of unique line segments, ensuring that overlapping segments are not double-counted.

```py
def countsegs(segset: set) -> int:
    ret, points = 0, set()
    for a, b, c, d in segset:
        ret += abs(a - c) + abs(b - d) + 1 - ((a, b) in points) - ((c, d) in points)
        points.update({(a, b), (c, d)})
    return ret
```

Finally, we combine both parts that return the output of the Dijkstra function that gives us the correct answer directly:
```py
class Solution(StrSplitSolution):
    def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        start = list(grid.keys())[list(grid.values()).index("S")]
        end = list(grid.keys())[list(grid.values()).index("E")]
        return dijkstra(grid, start, end)
```