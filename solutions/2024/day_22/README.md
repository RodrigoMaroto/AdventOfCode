# Day 22 (2024)

`Monkey Market` ([prompt](https://adventofcode.com/2024/day/22))

Use this space for notes on the day's solution and to document what you've learned!

## Part 1
Today's puzzle involves manipulating a series of numbers using a pseudo-random transformation function. The goal is to process each input number through 2000 iterations of the secret_num function and sum the resulting values.

The `secret_num` function generates a pseudo-random transformation of the input value using bitwise operations. The result is constrained to a 24-bit number using the mask `0xFFFFFF` at each step:

1. XOR the input with itself left-shifted by 6.
2. XOR the result with itself right-shifted by 5.
3. XOR the result with itself left-shifted by 11.
```py
def secret_num(n: int) -> int:
    n = (n ^ (n << 6)) & 0xFFFFFF
    n = (n ^ (n >> 5)) & 0xFFFFFF
    return (n ^ (n << 11)) & 0xFFFFFF
```
For each input number we execute this transformation 2000 times and sum the results as explained before.
```py
class Solution(IntSplitSolution):
    def part_1(self) -> int:
        result = 0
        for i in self.input:
            res = i
            for _ in range(2000):
                res = secret_num(res)
            result += res
        return result
```

## Part 2
Part 2 introduces additional complexity by analyzing patterns in the differences between successive transformations. The objective is to identify the pattern of length 4 that provides the highest payout.  

First, we generate the sequences of pseudo-random numbers and compute their differences between succesive values. Then we analyze each pattern and calculate the payout for each.  
```py
class Solution(IntSplitSolution):
    def part_2(self) -> int:
        result = defaultdict(int)
        for i in self.input:
            nums = [i] + [i := secret_num(i) for _ in range(2000)]
            diffs = [(b % 10) - (a % 10) for a, b in pairwise(nums)]
            seen = set()
            for i in range(len(nums) - 4):
                pat = tuple(diffs[i : i + 4])
                if pat not in seen:
                    result[pat] += nums[i + 4] % 10
                    seen.add(pat)
        return max(result.values())
```
