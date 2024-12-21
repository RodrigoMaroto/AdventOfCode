# Day 17 (2024)

`Chronospatial Computer` ([prompt](https://adventofcode.com/2024/day/17))

Today's puzzle involves simulating a simple low-level programming language executed on a hypothetical machine with 3 registers and 8 different instruction types.

## Part 1
The `execute_instruction` function interprets and executes a single instruction. The instructions are defined using an opcode, and depending on the opcode, the machine performs operations such as arithmetic, bitwise operations, or jumps with an operand. After processing an instruction, the `pointer` is updated to move to the next instruction.
```py
def execute_instruction(
    instructions: list[int], pointer: int, combo_op, out_buffer
) -> int:
    match instructions[pointer]:
        case 0:
            combo_op[4] = combo_op[4] // (2 ** combo_op[instructions[pointer + 1]])
        case 1:
            combo_op[5] = combo_op[5] ^ instructions[pointer + 1]
        case 2:
            combo_op[5] = combo_op[instructions[pointer + 1]] % 8
        case 3:
            if combo_op[4] != 0:
                pointer = instructions[pointer + 1] - 2
        case 4:
            combo_op[5] = combo_op[5] ^ combo_op[6]
        case 5:
            out_buffer.append(combo_op[instructions[pointer + 1]] % 8)
        case 6:
            combo_op[5] = combo_op[4] // (2 ** combo_op[instructions[pointer + 1]])
        case 7:
            combo_op[6] = combo_op[4] // (2 ** combo_op[instructions[pointer + 1]])
    pointer += 2
    return pointer
```
The `execute_program` function coordinates the execution of all instructions. It initializes the machine state, including the registers (`combo_op`) and the output buffer (`out_buffer`). It then processes the instruction list iteratively until all instructions have been executed.
```py
def execute_program(
    instructions: list[int], a: int, b: int = 0, c: int = 0
) -> list[int]:
    combo_op = {0: 0, 1: 1, 2: 2, 3: 3, 4: a, 5: b, 6: c}
    out_buffer = []
    pointer = 0
    while pointer < len(instructions):
        pointer = execute_instruction(instructions, pointer, combo_op, out_buffer)
    return out_buffer
```
The input contains initial values for registers `a`, `b`, and `c`, followed by the list of instructions. The `execute_program` function is called to process these instructions and produce the output buffer, which is then converted to a comma-separated string.
```py
class Solution(TextSolution):
    def part_1(self) -> str:
        a, b, c, *instructions = [int(x) for x in re.findall(r"\d+", self.input)]
        out_buffer = execute_program(instructions, a, b, c)
        return ",".join([str(x) for x in out_buffer])
```

## Part 2
In Part 2, the challenge is to find the initial value of Register A (`a`) that makes the output of the program exactly match the instruction list. This involves recursively testing potential values of `a` while ensuring the program produces the desired output.

An important note, is that if you reverse engineer the given code, the output of each iteration only depends on the value of Register A, and more importantly, it only consumes and therefore takes into account 3 bits.  

Therefore, the `find_a` function implements a depth-first search to identify the correct value for a. Starting from an initial value, the function recursively tests different values by appending digits (in base 8) and checking if the output matches the target. We can observe:
- Base Case: If the recursion depth matches the length of the reversed target instruction list, the function returns the current value of `a` as the solution.
- Recursive Case: 
    For each possible value of the least significant digit (0 through 7), the function executes the program with the current candidate for a, compares the first output value to the corresponding reversed instruction value and recursively calls itself with the updated value of a (multiplied by 8 to add the new digit) and increased depth.

```py
def find_a(instructions: list[int], a: int = 0, depth: int = 0) -> int:
    target = instructions[::-1]
    if depth == len(target):
        return a
    for i in range(8):
        output = execute_program(instructions, a * 8 + i)
        if (
            output
            and output[0] == target[depth]
            and (result := find_a(instructions, (a * 8 + i), depth + 1))
        ):
            return result
    return 0
```
Finally, I combined the result of both parts in a single function.
```py
class Solution(TextSolution):
    def solve(self) -> tuple[int, int]:
        a, b, c, *instructions = [int(x) for x in re.findall(r"\d+", self.input)]
        out_buffer = execute_program(instructions, a, b, c)
        return ",".join([str(x) for x in out_buffer]), find_a(instructions)
```

