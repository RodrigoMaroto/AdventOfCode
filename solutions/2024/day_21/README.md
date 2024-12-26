# Day 21 (2024)

`Keypad Conundrum` ([prompt](https://adventofcode.com/2024/day/21))

Use this space for notes on the day's solution and to document what you've learned!

## Part 1
In Part 1, the task is to determine the total weighted distance across all input codes when navigating the numeric and directional keypads.

Two separate keypads are defined:
- Numeric Keypad:
A traditional phone-style layout with digits and additional symbols (`A` for confirm and space for gap).
- Directional Keypad:
A 2x3 grid used to represent directional movements (`^`, `v`, `<`, `>`).
```py
num_pad = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
    " ": (3, 0), "0": (3, 1), "A": (3, 2),
}

dir_pad = {
    " ": (0, 0), "^": (0, 1), "A": (0, 2),
    "<": (1, 0), "v": (1, 1), ">": (1, 2),
}
```
The `shortestPath` function computes the optimal sequence of movements to navigate between two keys. Such optimal instructions have several characteristics:
1. The instruction sequence must terminate with an `A` (to get the next robot to actually do the thing we want it to)
2. Any given instruction sequence that transitions from one key to another may contain `<` or `>` instructions but never both (that would be inefficient). And similarly, vertical movement may contain `v` or `^` instructions, but never both.
3. Since the cheapest transition is one that stays in the same location, the optimal path will be the one that groups repeated direction instructions. For example from `A` to `<` it is cheaper to be instructed to go `v<<` than it is to go `<v<`.
4. A path must never transit the gap in the keypad.

Credits for help with this problem to [Jo Wood](https://observablehq.com/@jwolondon/advent-of-code-2024-day-21).

```py
def shortestPath(key1: str, key2: str, isNumPad: bool) -> str:
    pad = num_pad if isNumPad else dir_pad
    r1, c1 = pad[key1]
    r2, c2 = pad[key2]

    ud = "v" * (r2 - r1) if r2 > r1 else "^" * (r1 - r2)
    lr = ">" * (c2 - c1) if c2 > c1 else "<" * (c1 - c2)

    if c2 > c1 and (r2, c1) != pad[" "]:
        # Safe to move vertically first if heading right and corner point isn't the gap
        return ud + lr + "A"

    if (r1, c2) != pad[" "]:
        # Safe to move horizontally first if corner point isn't the gap
        return lr + ud + "A"
    # Must be safe to move vertically first because we can't be in same column as gap.
    return ud + lr + "A"
```
The solve function is a recursive function with memoization that returns the length of the string generated after `d` intermediate robots (`2` for Part 1).

- Base case: If the current level `l` is greater than the maximum depth `d`, the function returns the length of the input string `s`
- Recursive case: If the base case is not met, the function recursively calls itself for each pair of characters in the input string s. Here's what happens:

    - `zip('A' + s, s)` pairs each character in the input string `s` with the corresponding character in the string `'A' + s`. This is done to create pairs of characters that need to be processed.
    - For each pair of characters `(f, t)`, the function calls `shortestPath(f, t, False if l else True)` to compute the shortest path between the two characters. When `l` is zero it is the only time we use a numerical keypad, so the argument `isNumPad` is `True`.
    - The solve function is then called recursively with the shortest path as the new input string `s`, the current level `l` incremented by 1, and the same maximum depth `d`.
    - The results of these recursive calls are summed up using the `sum` function.

```py
@cache
def solve(s: str, l: int, d: int) -> int:
    if l > d:
        return len(s)
    return sum(solve(shortestPath(f, t, not l), l + 1, d) for f, t in zip("A" + s, s))
```
Finally, to obtain the solution we have to add the result of the length of the generated instruction sequence multiplied by the initial numeric code, for each of the five codes provided in the input.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        return sum(solve(code, 0, 2) * int(code[:-1]) for code in self.input)
```

## Part 2
As our solution for Part 1, is already very general, we just need to change the `d` argument to represent the 25 intermediate robots that appear in this second part to obtain the solution.
```py
class Solution(StrSplitSolution):
    def part_2(self) -> int:
        return sum(solve(code, 0, 25) * int(code[:-1]) for code in self.input)
```
