# Day 6 (2024)

`Guard Gallivant` ([prompt](https://adventofcode.com/2024/day/6))

Yet another Grid challenge, throwing in some loop detection too!

## Part 1

Today for the input parsing, i decided to adopt the method invented by the creator of this template (you can check more information on it [here](https://advent-of-code.xavd.id/writeups/2024/day/4/)). The grid is represented as a `dict` where the keys are tuples of `(row, col)`, and the values are the characters at those positions.

 
```py
GridPoint = tuple[int, int]
Grid = dict[GridPoint, str]


def parse_grid(raw_grid: list[str]) -> Grid:
    result = {}

    for row, line in enumerate(raw_grid):
        for col, c in enumerate(line):
            result[row, col] = c

    return result
```
With parsing out of the way, we can now focus on solving the problem. First, I created a small helper function to update the guard's walking direction. According to the instructions, the guard rotates 90º clockwise when encountering an obstacle. I store the direction as an offset used to calculate the position at each iteration.
```py
def update_direction(direction: tuple[int, int]) -> tuple[int, int]:
    if direction[1] == 0:
        return (0, -direction[0])
    return (direction[1], 0)
```
In Part 1, we need to count how many unique positions the guard passes through. To accomplish this, we store the visited positions in a `set` and return its length at the end.

To track the movements, we:

1. Identify the starting position and direction.
2. Use a loop to repeatedly compute the next position.
3. Store each visited position.
4. Check if the next position is valid:
    - If it's outside the grid, exit the loop.
    - If it contains an obstacle (`"#"`), update the direction and skip to the next iteration.
    - Otherwise, update the guard's position and continue.  

Here’s the implementation:
```py
def track_guard(grid: Grid) -> int:
    guard_pos = list(grid.keys())[list(grid.values()).index("^")]
    guard_direction = (-1, 0)
    visited = set()

    while True:
        visited.add(guard_pos)
        new_pos = (guard_pos[0] + guard_direction[0], guard_pos[1] + guard_direction[1])

        if new_pos not in grid:
            break

        if grid[new_pos] == "#":
            guard_direction = update_direction(guard_direction)
            continue

        guard_pos = new_pos

    return len(visited)

class Solution(StrSplitSolution):
    def part_1(self) -> int:
        grid = parse_grid(self.input)
        return track_guard(grid)
```

## Part 2
In this part we need to identify loops in  the guards path. To achieve this, the `track_guard` function is updated to track not only the positions visited by the guard but also the direction at each step. By doing this, we can detect when the guard revisits a position while facing the same direction, which would indicate a loop. The changes I added are: 

1. **Tracking Direction in Addition to Position**:
In the updated function, the visited set stores tuples of both the guard's position and its direction at that step, e.g., (guard_pos, guard_direction). This ensures that revisiting the same position but from a different direction does not falsely trigger a loop.

2. **Loop Detection**:
Each new position and direction is checked against the visited set. If the current (guard_pos, guard_direction) is already in the set, a loop is detected. In this case:
    - The function returns False, indicating a loop.
    - It also returns an empty set to signal no valid path without a loop.  

3. Valid Path Handling:
If no loop is detected, the function proceeds normally:
    - It records all visited positions (ignoring the direction) in the returned set.
    - It returns True to indicate the path was loop-free.

The function now returns a tuple:
- he first value is a boolean indicating whether the path is loop-free (`True`) or contains a loop (False).
- The second value is either a set of visited positions (if loop-free) or an empty set (if a loop is detected).

```py
def track_guard_old(grid: Grid) -> tuple[bool, set]:
    guard_pos = list(grid.keys())[list(grid.values()).index("^")]
    guard_direction = (-1, 0)
    visited = set()

    while True:
        visited.add((guard_pos, guard_direction))
        new_pos = (guard_pos[0] + guard_direction[0], guard_pos[1] + guard_direction[1])

        if new_pos not in grid:
            break

        if grid[new_pos] == "#":
            guard_direction = update_direction(guard_direction)
            visited.add((guard_pos, guard_direction))

        else:
            to_add = new_pos, guard_direction
            if to_add in visited:
                # loop!
                return False, set()

            visited.add(to_add)
            guard_pos = new_pos

    return True, {l for l, _ in visited}
```

With this function, we can now first obtain the original path, and add obstacles in each of those positions to attempt to generate loops.  

This brute force solution takes a bit of time but I consider that it is within a reasonable range.

```py
def part_2(self) -> int:
        grid = parse_grid(self.input)
        _, path = track_guard(grid)
        result = 0
        for pos in path:
            if grid[pos] == "^":
                continue
            grid[pos] = "#"
            if not track_guard(grid)[0]:
                result += 1
            grid[pos] = "."

        return result
```

