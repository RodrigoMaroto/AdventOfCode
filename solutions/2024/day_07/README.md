# Day 7 (2024)

`Bridge Repair` ([prompt](https://adventofcode.com/2024/day/7))

First day this year where I attempt to brute force a problem and have to rethink it.

## Part 1
Today we are given a list of equations that contain a result and a list of operands. Our task is to determine whether any combination of these operands, using the operators `+` (addition) and `*` (multiplication), can produce the given result.    

To solve this, I implemented a recursive function that evaluates the equation from right to left, effectively pruning many unnecessary permutations during the process.

The function valid_equation takes two arguments: the target result and a list of operands. It recursively explores whether the target result can be obtained by combining the operands with either addition or multiplication.

1. Base Case:
When only one operand remains, the function checks if it equals the target result. If it does, the function returns True.

2. Recursive Case:
    - Multiplication: If the target result is divisible by the last operand, the function recursively checks whether the quotient (result divided by the last operand) can be formed using the remaining operands.
    - Addition: The function also checks whether the difference (result minus the last operand) can be formed using the remaining operands.  

The function returns True if either operation is successful, effectively pruning paths that cannot produce the target result.

```py
def valid_equation(result: int, operands: list[int]) -> bool:
    if len(operands) == 1:
        return operands[0] == result

    last = operands[-1]

    if result % last == 0:
        possible_mul = valid_equation(result // last, operands[:-1])
    else:
        possible_mul = False

    possible_add = valid_equation(result - last, operands[:-1])

    return possible_mul or possible_add
```

To obtain the required solution we add the results of the valid equations:

```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        sol = 0
        for line in self.input:
            result, operands = line.split(": ")
            result = int(result)
            operands = [int(x) for x in operands.split(" ")]
            if valid_equation(result, operands, False):
                sol += result
        return sol
```

## Part 2

For this part 2, We extend the functionality of our solution to support a new operator, `|` (concatenation), which combines two integers by appending one to the other. For example, `12 | 345` results in `12345`.

The updated function valid_equation now includes logic to handle concatenation. Here's how it works:

1. Multiplication and Addition: These cases remain unchanged and are evaluated as before.
2. Concatenation:
    - We compute a "shift factor" based on the number of digits in the last operand. This allows us to verify whether the target result can be decomposed into a concatenation of the last operand and a previous result.
    - If the concatenation is valid, the function recursively checks whether the remainder can be formed using the remaining operands.

The new argument `check_concat` allows for compatibility with Part 1.

```py
def valid_equation(result: int, operands: list[int], check_concat: bool = True) -> bool:
    ...

    possible_concat = False
    if check_concat:
        shift = 10 ** len(str(last))
        if (result - last) % shift == 0:
            possible_concat = valid_equation((result - last) // shift, operands[:-1])

    return possible_mul or possible_add or possible_concat
```

