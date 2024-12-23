# Day 19 (2024)

`Linen Layout` ([prompt](https://adventofcode.com/2024/day/19))

Today’s challenge is about matching and combining patterns to recreate designs. Part 1 involves determining whether each design can be formed using the given patterns, while Part 2 focuses on counting the number of ways to do so.

## Part 1
In Part 1, the task is to determine if each design can be created using a set of patterns. Each pattern can be used multiple times, and the designs must be formed by concatenating these patterns in order.  

The `possible` function determines whether a target design can be formed using the given patterns:
- Base Case: If the `target` is empty, it means the design can be formed.
- Recursive Case: For each pattern in `patterns`, check if the target starts with that pattern. If so, recursively check the rest of the target (after removing the matched pattern).
The function uses caching (`functools.cache`) to optimize repeated calls with the same inputs, using the principles of Dynammic Programming (DP).
```py
@cache
def possible(patterns: tuple[str, ...], target: str) -> bool:
    if not target:
        return True
    return any(
        possible(patterns, target[len(pat) :])
        for pat in patterns
        if target.startswith(pat)
    )
```
To find the solution we parse the input and run the `possible` function for each of the target designs.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        patterns, _, *designs = self.input
        patterns = tuple(x.strip() for x in patterns.split(","))
        return sum(possible(patterns, d) for d in designs)
```

## Part 2
In Part 2, the focus shifts to counting the number of ways each design can be formed using the given patterns.
The `combs` function counts all possible combinations of patterns that can form the target design:
- Base Case: If the `target` is empty, there is exactly one way to form the design (using no patterns).
- Recursive Case: For each pattern in `patterns`, check if the target starts with that pattern. If so, recursively count the combinations for the rest of the target.
```py
@cache
def combs(patterns: tuple[str, ...], target: str) -> int:
    if not target:
        return 1
    return sum(
        combs(patterns, target[len(pat) :])
        for pat in patterns
        if target.startswith(pat)
    )
```
To combine both solutions, we can add the results of the function for Part 2 and determine the length of the array after getting rid of those patterns that are impossible (`0` combinations).
```py
class Solution(StrSplitSolution):
    def solve(self) -> tuple[int, int]:
        patterns, _, *designs = self.input
        patterns = tuple(x.strip() for x in patterns.split(","))
        combinations = [x for d in designs if (x := combs(patterns, d)) != 0]
        return len(combinations), sum(combinations)
```