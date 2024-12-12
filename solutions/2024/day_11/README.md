# Day 11 (2024)

`Plutonian Pebbles` ([prompt](https://adventofcode.com/2024/day/11))

Today was a nice problem where brute-force became impossible for Part 2, and I had to re-do my solution. Additionally, I saw on Reddit some solutions that used more complex mathematical tools like State Transition Matrix (STM) that are also very interesting.

## Part 1
Today the input consists on a list of integers that is transformed in each iteration following the same subset of rules:
- If the number is `0`, it is replaced by the number `1`.
- If the number has an even number of digits, it is replaced by two numbers. The left half of the digits on the first, and the right half of the digits on the second. (The new numbers don't keep extra leading zeroes: 1000 would become 10 and 0.)
- If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by `2024` is engraved on the new stone.

Therefore, I just created a very simple function that would update the array and execute it 25 times to obtain the correct solution.
```py
def update_stones(stones: list[int]) -> list[int]:
    result = []
    for stone in stones:
        if stone == 0:
            result.append(1)
        elif (length := len(str(stone))) % 2 == 0:
            result.append(int(str(stone)[: length // 2]))
            result.append(int(str(stone)[length // 2 :]))
        else:
            result.append(stone * 2024)
    return result

class Solution(IntSplitSolution):
    def part_1(self) -> int:
        stones = self.input.copy()
        for _ in range(25):
            stones = update_stones(stones)
        return len(stones)
```

## Part 2
This brute-force solution would stop working on a reasonable ammount of time when executed for more than 30-32 iterations. This is obviously very far from the required `75` loops, so I moved to a more elegant solution based on recursion and memoization, otherwise also known as dynamic programming.

To explain memoization before going into the function itself, it will basically cache or store the arguments and the result everytime the function is called. Thanks to this, if the same arguments are passed again, it will simply return the value stored in memory instead of computing it again. This is very easily done in Python thanks to  `functools.cache` but could also be coded using a `dict` structure.

The `solve` function I created will now process each of the numbers independently as they have no interdependence with each other and its objective is to return the final number of integers that would appear by following the rules.

The base case is when the iterations ("blinks" in the problem description) reach '0' where it will simply return 1. In the cases where the integer is not split it will call itself updating the value and the number of blinks left. And finally, when it is split, it will add the results fo both generated numbers called recursively.

```py
@cache
def solve(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    if stone == 0:
        return solve(1, blinks - 1)
    if len(str_stone := str(stone)) % 2 == 0:
        mid = len(str_stone) // 2
        return solve(int(str_stone[:mid]), blinks - 1) + solve(
            int(str_stone[mid:]), blinks - 1
        )
    return solve(stone * 2024, blinks - 1)
```

We can group both solutions which will speed it up even more thanks to the memoization explained before.
```py
class Solution(IntSplitSolution):
    def solve(self) -> tuple[int, int]:
        return sum(solve(stone, 25) for stone in self.input), sum(
            solve(stone, 75) for stone in self.input
        )
```
