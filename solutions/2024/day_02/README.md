# Day 2 (2024)

`Red-Nosed Reports` ([prompt](https://adventofcode.com/2024/day/2))

Quite simple solution for Part 1 and for Part 2 I simply opted to reuse the previous solution, although probably more elegant solutions are possible.

## Part 1
For the input handling, today we have a list of integers in each line that will also be treated separately so I created a `list[list[int]]` structure as we can see here:
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        reports = [list(map(int, line.split())) for line in self.input]
```

For the solution, we need to classify each report as __Safe__ or __Unsafe__ based on this two citeria:

- The levels are either all increasing or all decreasing.
- Any two adjacent levels differ by at least one and at most three.

In a simpler way, these reports have to be sorted and we need to check the differences between elements, for which we will use and auxilary function.
```py
def safe_report(report: list[int]) -> bool:
    if report != sorted(report) and report != sorted(report, reverse=True):
        return False
    for i in range(len(report) - 1):
        diff = abs(report[i] - report[i + 1])
        if not 1 <= diff <= 3:
            return False
    return True
```
The way of performing the first check is not very efficient as we are sorting twice lists which has higher complexity than the linear check that is required. We can fix it like this:
```py
def is_sorted(report: list[int]) -> bool:
    if report[1] >= report[0]:  # increasing
        return all(report[i] <= report[i + 1] for i in range(len(report) - 1))
    # decreasing
    return all(report[i] >= report[i + 1] for i in range(len(report) - 1))

def safe_report(report: list[int]) -> bool:
    if not is_sorted(report):
        return False
    ...
```
  
To obtain the result, just need some elegant list comprehension to run this function with every report and count the valid ones.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        reports = [list(map(int, line.split())) for line in self.input]
        return sum([safe_report(report) for report in reports])
```

## Part 2

For this second part, we need to adapt the previous criteria to **tolerate a single bad level**, or in other words, check if the report would be safe if we remove one of the numbers.

In order to do this, we can simply use the previous `safe_report` function while giving it different inputs like this:
```py
def safe_report2(report: list[int]) -> bool:
    if safe_report(report):
        return True
    for i in range(len(report)):
        report_cp = report.copy()
        report_cp.pop(i)
        if safe_report(report_cp):
            return True
    return False
```
Finally we group both solutions as the input handling is identical in the `solve` function:

```py
class Solution(StrSplitSolution):
    def solve(self) -> tuple[int, int]:
        reports = [list(map(int, line.split())) for line in self.input]
        part1 = sum([safe_report(report) for report in reports])
        part2 = sum([safe_report2(report) for report in reports])
        return part1, part2
```
