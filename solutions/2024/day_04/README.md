# Day 4 (2024)

`Ceres Search` ([prompt](https://adventofcode.com/2024/day/4))

Today we have a traditional word search puzzle and a slightly different version for Part 2.

## Part 1
In this first part, we have to search for the word `XMAS` in a matrix that can appear horizontally, vertically, diagonally, written backwards, or even overlapping other words.

First, to handle the input, I transformed it into a matrix of characters. Additionally, when I need to do checks regarding adjacent elements in a matrix, I like to add a sort of outer layer (in this case, I will use `"."`) to forget about boundary checks.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        matrix = [["."] + list(line) + ["."] for line in self.input]
        matrix.insert(0, ["."] * len(matrix[0]))
        matrix.append(["."] * len(matrix[0]))
```
Once we have this, I simply applied my favorite way of traditionally solving these problems by hand, which is to look for all instances of the first character and try to follow all directions looking for the correct pattern.

For this, I created a function that, given the matrix and a position in it, will return the number of correct patterns found originating from there, and `0` if that element is different from `X`.

By solving it this way, we ensure that we capture all occurrences as words can overlap while taking care of duplicate counting as we are looking just for the origin of the word.

```py
def check_xmas(matrix: list[list[str]], x: int, y: int) -> int:
    if matrix[y][x] != "X":
        return 0
    valid_count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (
                matrix[y + i][x + j] == "M"
                and matrix[y + i * 2][x + j * 2] == "A"
                and matrix[y + i * 3][x + j * 3] == "S"
            ):
                valid_count += 1
    return valid_count

class Solution(StrSplitSolution):
    def part_1(self) -> int:
        ...
        return sum(
            check_xmas(matrix, x, y)
            for y in range(len(matrix))
            for x in range(len(matrix[0]))
        )
```

## Part 2

For Part 2, the pattern we need to find in this matrix is slightly different. It is defined as `X-MAS`, two `MAS` in the shape of an X. There are, therefore, 4 possibilities:
```
M.S     M.M     M.M     S.S   
.A.     .A.     .A.     .A.   
M.S     S.S     S.S     M.M   
```

Following a similar approach as the previous part, in this case, we identify `A` as the *origin* of the "word" and for each of these elements, we check if it is a valid combination. In this case, one of these can only be part of a single word and therefore our function now returns a boolean.  
We perform this check by assuring that in each diagonal there is both an `M` and an `S`, using a `set` to compare as we don't take the order into account.

```py
def check_x_mas(matrix: list[list[str]], x: int, y: int) -> bool:
    if matrix[y][x] != "A":
        return False
    return {matrix[y + 1][x + 1], matrix[y - 1][x - 1]} == {"M", "S"} and {
        matrix[y + 1][x - 1], matrix[y - 1][x + 1]} == {"M", "S"}

class Solution(StrSplitSolution):
    def solve(self) -> tuple[int, int]:
        matrix = [["."] + list(line) + ["."] for line in self.input]
        matrix.insert(0, ["."] * len(matrix[0]))
        matrix.append(["."] * len(matrix[0]))
        part1 = sum(
            check_xmas(matrix, x, y)
            for y in range(len(matrix))
            for x in range(len(matrix[0]))
        )
        part2 = sum(
            check_x_mas(matrix, x, y)
            for y in range(len(matrix))
            for x in range(len(matrix[0]))
        )
        return part1, part2
```
