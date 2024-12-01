# Day 1 (2024)

`Historian Hysteria` ([prompt](https://adventofcode.com/2024/day/1))

Very straightforward Day 1 to get into the Advent of Code rythm.

## Part 1
In order to handle the input I prefer to use this kind of easily readable and traditional solutions as opposed to other more _pythonic_ ways using functions like `map` or `zip`.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        left_list, right_list = [], []
        for line in self.input:
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))
```
To obtain the result we need to compare the ordered elements of both lists and return the sum of the differences between them. In Python this is very simple as there are built-in `sort` methods.

```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        ...

        left_list.sort()
        right_list.sort()
        return sum([abs(left_list[i] - right_list[i]) for i in range(len(left_list))])
```

## Part 2

For this part 2 the input handling will stay the same, but we need to compare the occurences of the elements of the left column in the right one.  
For this the best option is to use [`collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) which is a dictionary-like object that counts the occurences in any given iterable. It also returns 0 for a missing element as opposed to returning a `KeyError` (similar to `collections.defaultdict`)
```py
class Solution(StrSplitSolution):
    def part_2(self) -> int:
        ...

        right_count = Counter(right_list)
        return sum([right_count[num] * num for num in left_list])
```