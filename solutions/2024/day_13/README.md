# Day 13 (2024)

`Claw Contraption` ([prompt](https://adventofcode.com/2024/day/13))

A math solution applying some basic linear algebra!

## Part 1
Today the input, after parsing it, consists on a series of systems composed of two linear equations that we need to solve. As it is a 2x2 matrix the easiest way is to apply [Cramer's Rule](https://en.wikipedia.org/wiki/Cramer%27s_rule). Additionally, our solutions must be integers so we discard any that do not comply with this requirement in our helper function, returning `(0, 0)` instead.

For the input handling, we simply extract the six numbers that are relevant with the use of *regex*.
```py
def cramer_solution(
    button_a: list[int], button_b: list[int], prize: list[int]
) -> tuple[int, int]:
    det = button_a[0] * button_b[1] - button_b[0] * button_a[1]
    x = (prize[0] * button_b[1] - button_b[0] * prize[1]) / det
    y = (button_a[0] * prize[1] - prize[0] * button_a[1]) / det
    if x % 1 == 0 and y % 1 == 0:
        return int(x), int(y)
    return 0, 0

class Solution(StrSplitSolution):
    def part_1(self) -> int:
        data = [[int(i) for i in re.findall(r"\d+", s)] for s in self.input]
        result = 0
        for d in data:
            a, b = cramer_solution(d[0:2], d[2:4], d[4:])
            result += a * 3 + b
        return result
```

## Part 2
In part 2, the input positions for the "prize" have to be updated to the current value plus `10000000000000` to avoid brute-force solutions that would have been valid for Part 1. As our solution is a mathemathical approach, we simply need to combine both solutions. Additionally, I included some list comprehension to make it a bit more *pythonic*

```py
def solve(self) -> tuple[int, int]:
    data = [[int(i) for i in re.findall(r"\d+", s)] for s in self.input]
    part1 = sum(
        a[0] * 3 + a[1]
        for d in data
        if (a := cramer_solution(d[0:2], d[2:4], d[4:]))
    )
    for line in data:
        line[-1] += 10000000000000
        line[-2] += 10000000000000
    part2 = sum(
        a[0] * 3 + a[1]
        for d in data
        if (a := cramer_solution(d[0:2], d[2:4], d[4:]))
    )
    return part1, part2

```
