# Day 20 (2024)

`Race Condition` ([prompt](https://adventofcode.com/2024/day/20))

Today we are also using Dijkstra's Algoritm but in this case to precompute distances between all nodes.

## Part 1
In Part 1, cheating is allowed for two picoseconds. The task is to count the number of valid cheats where the time saved is more than 100 picoseconds.
The solution uses Dijkstra's algorithm to calculate the shortest distance from the start (`S`) to the end (`E`) for all reachable points on the grid:
- A priority queue processes each point, ensuring nodes are visited in increasing order of distance.
- The distances to all points are stored in a dictionary.
```py
def dijkstra(grid, start):
    distances = defaultdict(lambda:(float("inf")))
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]
    distances[start] = 0
    queue = [(0, start)]
    while queue:
        dist, pos = heapq.heappop(queue)
        for ndi in dirs:
            npos, ndist = add_points(pos, ndi), dist + 1
            if grid[npos] != "#":
                o_dist = distances[npos]
                if o_dist >= ndist:
                    distances[npos] = ndist
                    heapq.heappush(queue, (ndist, npos))
    return dict(distances)
```
To obtain the result, for each pair of points on the track, the Manhattan distance (`d`) between them is calculated:

- If `d == 2` (cheating for two picoseconds is possible).
- If the time saved (`j - i - d`, where `i` and `j` are the distances from the start to the respective points) exceeds 100 picoseconds, it counts as a valid cheat.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        grid = parse_grid(self.input)
        start = list(grid.keys())[list(grid.values()).index("S")]
        distances = dijkstra(grid, start)
        result = 0
        for (p,i), (q,j) in combinations(distances.items(), 2):
            d = manhattan(p, q)
            if d == 2 and j-i-d >= 100: result += 1
        return result
```

## Part 2
In Part 2, the cheating allowance increases to 20 picoseconds so we simply need to tune slightly our Part 1 to combine both of them.
```py
class Solution(StrSplitSolution):
    def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        start = list(grid.keys())[list(grid.values()).index("S")]
        distances = dijkstra(grid, start)
        result1, result2 = 0, 0
        for (p,i), (q,j) in combinations(distances.items(), 2):
            d = manhattan(p, q)
            if d == 2 and j-i-d >= 100: result1 += 1
            if d < 21 and j-i-d >= 100: result2 += 1
        return result1, result2
```