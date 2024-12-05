# Day 5 (2024)

`Print Queue` ([prompt](https://adventofcode.com/2024/day/5))

A typical sorting problem in AoC, which helped me learn about yet another great function from Python's `stdlib`.

## Part 1
The input is divided into two parts: **rules** and **updates**. The rules are pairs of integers that define precedence requirements: the first number in a pair must appear in the update before the second for the update to be considered valid.
To store these rules, I used a `dict` where each key is a page number, and the corresponding value is a `set` containing all its precedent numbers. Using a `set` avoids duplicate rules, which could otherwise slow down processing. Here's an example of the structure:
```
97|13       
61|13       {
75|53       13: {97, 61, 29}
29|13   =>  53: {75, 47}
47|53       47: {97}
97|47       }
```
Updates are simply lists of integers, so there’s nothing particularly complex there. The input handling looks like this:
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        index = self.input.index("")
        rules_list, updates = (
            self.input[:index],
            [[int(x) for x in line.split(",")] for line in self.input[index + 1 :]],
        )

        rules = defaultdict(set)
        for rule in rules_list:
            l, r = map(int, rule.split("|"))
            rules[r].add(l)
```

In this part, the task is to identify valid updates. To achieve this, I implemented a `valid_update` function that returns a boolean. For each element in an update, the function checks if it has any precedence rules. If it does, it ensures that the rules are satisfied by comparing indexes.

```py
def valid_update(update: list[int], rules: dict[int, set[int]]) -> bool:
    for i, elem in enumerate(update):
        if elem not in rules:
            continue
        for rule in rules[elem]:
            if rule in update and i < update.index(rule):
                return False
    return True
```

The problem asks us to return the sum of the **middle element** of the valid updates, so we do that with some list comprehension and we have our Part 1 done!

```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        ...
        return sum(
            update[len(update) // 2]
            for update in updates
            if valid_update(update, rules)
        )
```

## Part 2
In the second part, we are tasked with reordering the incorrect pages. Initially, I implemented a custom sorting function to resolve individual conflicts. While functional, this approach required too many iterations and was noticeably slow. Here's the original function:

```py
def reorder_update(update: list[int], rules: dict[int, set[int]]) -> list[int]:
    for _ in update:
        for i, elem in enumerate(update):
            if elem not in rules:
                continue
            for rule in rules[elem]:
                if rule in update and i < (idx := update.index(rule)):
                    update.insert(idx + 1, elem)
                    update.pop(i)
                    break
    return update
```

To optimize this, I leveraged `functools.cmp_to_key`, which allows us to use a custom comparison function with Python's built-in `sorted` function.

```
Note: A comparison function is any callable that accepts two arguments and compares them. A key function is a callable that accepts one argument and returns another value to be used as the sort key.
```

For the comparison function, the requirements are straightforward:

- It must accept two arguments `(a, b)`.
- Return a positive integer if `a > b`, a negative integer if `a < b`, and `0` if they are equal.  

In this context, a page with precedence is considered less than its dependent pages. Here's the implementation:

```py
def comparator(a, b):
    if b in rules[a]:
        return 1
    if a in rules[b]:
        return -1
    return 0
```
Using this comparator, the sorting process becomes efficient and integrates seamlessly with the solution. Combining both parts of the problem, the final implementation looks like this:

```py
def solve(self) -> tuple[int, int]:
    ... # Input handling

    part1, part2 = 0, 0

    for update in updates:
        if valid_update(update, rules):
            part1 += update[len(update)//2]
        else:
            part2 += sorted(update, key=cmp_to_key(comparator))[len(update)//2]

    return part1, part2
```
