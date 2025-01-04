# Day 25 (2024)

`Code Chronicle` ([prompt](https://adventofcode.com/2024/day/25))

Straightforward puzzle to end this year's Advent Of Code.

## Part 1
Today’s challenge involves analyzing schematics of locks and keys to determine which keys fit which locks. Each lock and key is represented as a grid of `#` and `.` characters. The task is to determine the number of unique lock/key pairs that fit together without overlapping.

The function `parse_heights` extracts the heights of locks or keys from the grid representation. It transposes the grid using `zip` to analyze columns instead of rows. Count the number of `#` characters for each column, subtracting  to exclude the top row (for locks) or bottom row (for keys).
```py
def parse_heights(grid: str) -> tuple[int, ...]:
    return tuple(col.count("#") - 1 for col in zip(*grid.split("\n")))
```
The function `fits` checks if a given key fits a lock by iterating through the corresponding heights of the lock and key, ensuring that for all columns, the sum of the heights does not exceed 5.

```py
def fits(key: tuple[int, ...], lock: tuple[int, ...]) -> bool:
    return all((l + k <= 5 for l, k in zip(lock, key)))
```
Finally we can see the solution implementation, where I use the `parse_heights` function to create to lists: `locks` and `keys`, depending on whether the top row contained a `#`. To obtain the solution we only need to apply the `fits` function to all different pairs of elements in these two lists.  
```py
class Solution(TextSolution):
    def part_1(self) -> int:
        grids = self.input.split("\n\n")
        locks, keys = [], []
        for i in grids:
            if i[0] == "#":
                locks.append(parse_heights(i))
            else:
                keys.append(parse_heights(i))
        return sum(fits(key, lock) for lock in locks for key in keys)
```