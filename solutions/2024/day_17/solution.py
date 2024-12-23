# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/17

import re

from ...base import TextSolution, answer


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


def execute_program(
    instructions: list[int], a: int, b: int = 0, c: int = 0
) -> list[int]:
    combo_op = {0: 0, 1: 1, 2: 2, 3: 3, 4: a, 5: b, 6: c}
    out_buffer = []
    pointer = 0
    while pointer < len(instructions):
        pointer = execute_instruction(instructions, pointer, combo_op, out_buffer)
    return out_buffer


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


class Solution(TextSolution):
    _year = 2024
    _day = 17

    @answer("4,3,7,1,5,3,0,5,4")
    def part_1(self) -> str:
        a, b, c, *instructions = [int(x) for x in re.findall(r"\d+", self.input)]

        out_buffer = execute_program(instructions, a, b, c)
        return ",".join([str(x) for x in out_buffer])

    @answer(190384615275535)
    def part_2(self) -> int:
        a, b, c, *instructions = [int(x) for x in re.findall(r"\d+", self.input)]

        return find_a(instructions, 0, 0)

    @answer(("4,3,7,1,5,3,0,5,4", 190384615275535))
    def solve(self) -> tuple[str, int]:
        a, b, c, *instructions = [int(x) for x in re.findall(r"\d+", self.input)]
        out_buffer = execute_program(instructions, a, b, c)
        return ",".join([str(x) for x in out_buffer]), find_a(instructions)
