# Day 14 (2024)

`Restroom Redoubt` ([prompt](https://adventofcode.com/2024/day/14))

Another math heavy solutionusing modular arithmetic.

## Part 1
The input handling is very similar to yesterday where we extract all of the integers using Regular expressions. After this we simulate the position of each particle after `100` iterations. Because when a particle goes over one of the sides it teleports to the contrary, this problem is perfect for modular arithmetic where our modules will be the maximum width and height.  

After we obtain the final positions, we determine which cuadrant they belong to and update its count. Finally we return the multiplication of all cuadrants using `math.prod` which works equivalently to `sum()`

```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        data = [[int(i) for i in re.findall(r"-?\d+", s)] for s in self.input]
        cuadrants = [0 for _ in range(4)]
        width = 101
        height = 103
        for i in data:
            x = (i[0] + i[2] * 100) % width
            y = (i[1] + i[3] * 100) % height
            if x < width//2:
                if y < height//2:
                    cuadrants[0] += 1
                elif y > height//2:
                    cuadrants[2] += 1
            elif x > width//2:
                if y < height//2:
                    cuadrants[1] += 1
                elif y > height//2:
                    cuadrants[3] += 1
        return math.prod(cuadrants)
```

## Part 2
For this part, i used the following explanation from [Reddit](https://www.reddit.com/r/adventofcode/comments/1he0asr/2024_day_14_part_2_why_have_fun_with_image/). This solution is based on the concept that when the tree-shaped image appears, it will be the same as the minimum variance between particles. 

```py
def simulate(t: int, width: int, height: int, robots: list[list[int]]) -> list[tuple[int, int]]:
    return [((sx + t*vx) % width, (sy + t*vy) % height) for (sx, sy, vx, vy) in robots]

def part_2(self) -> int:
    data = [[int(i) for i in re.findall(r"-?\d+", s)] for s in self.input]
    width = 101
    height = 103
    bx, bxvar, by, byvar = 0, 10*100, 0, 10*1000
    for t in range(max(width, height)):
        xs, ys = zip(*simulate(t, width, height, data))
        if (xvar := variance(xs)) < bxvar: bx, bxvar = t, xvar
        if (yvar := variance(ys)) < byvar: by, byvar = t, yvar
    return bx+((pow(width, -1, height)*(by-bx)) % height)*width
```
