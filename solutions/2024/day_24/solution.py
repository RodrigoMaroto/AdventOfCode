# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/24

from ...base import TextSolution, answer


def process(op: str, op1: bool, op2: bool) -> bool:
    if op == "AND":
        return op1 & op2
    if op == "OR":
        return op1 | op2
    # "XOR"
    return op1 ^ op2


class Solution(TextSolution):
    _year = 2024
    _day = 24

    @answer(45923082839246)
    def part_1(self) -> int:
        values, gates = self.input.split("\n\n")
        wires: dict[str, bool] = {}
        operations = []
        highest_z = "z00"
        for line in values.split("\n"):
            key, v = line.split(": ")
            wires[key] = bool(int(v))
        for line in gates.split("\n"):
            op1, op, op2, _, res = line.split(" ")
            operations.append((op1, op, op2, res))
            if res[0] == "z" and int(res[1:]) > int(highest_z[1:]):
                highest_z = res

        while len(operations):
            op1, op, op2, res = operations.pop(0)
            if op1 in wires and op2 in wires:
                wires[res] = process(op, wires[op1], wires[op2])
            else:
                operations.append((op1, op, op2, res))

        bits = [
            str(int(wires[wire]))
            for wire in sorted(wires, reverse=True)
            if wire[0] == "z"
        ]
        return int("".join(bits), 2)

    @answer("jgb,rkf,rrs,rvc,vcg,z09,z20,z24")
    def part_2(self) -> str:
        values, gates = self.input.split("\n\n")
        wires: dict[str, bool] = {}
        operations = []
        highest_z = "z00"
        for line in values.split("\n"):
            key, v = line.split(": ")
            wires[key] = bool(int(v))
        for line in gates.split("\n"):
            op1, op, op2, _, res = line.split(" ")
            operations.append((op1, op, op2, res))
            if res[0] == "z" and int(res[1:]) > int(highest_z[1:]):
                highest_z = res

        wrong = set()
        for op1, op, op2, res in operations:
            if res[0] == "z" and op != "XOR" and res != highest_z:
                wrong.add(res)
            if (
                op == "XOR"
                and res[0] not in ["x", "y", "z"]
                and op1[0] not in ["x", "y", "z"]
                and op2[0] not in ["x", "y", "z"]
            ):
                wrong.add(res)
            if op == "AND" and "x00" not in [op1, op2]:
                for subop1, subop, subop2, subres in operations:
                    if res in (subop1, subop2) and subop != "OR":
                        wrong.add(res)
            if op == "XOR":
                for subop1, subop, subop2, subres in operations:
                    if res in (subop1, subop2) and subop == "OR":
                        wrong.add(res)

        return ",".join(sorted(wrong))

    @answer((45923082839246, "jgb,rkf,rrs,rvc,vcg,z09,z20,z24"))
    def solve(self) -> tuple[int, str]:
        values, gates = self.input.split("\n\n")
        wires: dict[str, bool] = {}
        operations = []
        highest_z = "z00"
        for line in values.split("\n"):
            key, v = line.split(": ")
            wires[key] = bool(int(v))
        for line in gates.split("\n"):
            op1, op, op2, _, res = line.split(" ")
            operations.append((op1, op, op2, res))
            if res[0] == "z" and int(res[1:]) > int(highest_z[1:]):
                highest_z = res

        wrong = set()
        for op1, op, op2, res in operations:
            if res[0] == "z" and op != "XOR" and res != highest_z:
                wrong.add(res)
            if (
                op == "XOR"
                and res[0] not in ["x", "y", "z"]
                and op1[0] not in ["x", "y", "z"]
                and op2[0] not in ["x", "y", "z"]
            ):
                wrong.add(res)
            if op == "AND" and "x00" not in [op1, op2]:
                for subop1, subop, subop2, subres in operations:
                    if res in (subop1, subop2) and subop != "OR":
                        wrong.add(res)
            if op == "XOR":
                for subop1, subop, subop2, subres in operations:
                    if res in (subop1, subop2) and subop == "OR":
                        wrong.add(res)

        while len(operations):
            op1, op, op2, res = operations.pop(0)
            if op1 in wires and op2 in wires:
                wires[res] = process(op, wires[op1], wires[op2])
            else:
                operations.append((op1, op, op2, res))

        bits = [
            str(int(wires[wire]))
            for wire in sorted(wires, reverse=True)
            if wire[0] == "z"
        ]
        return int("".join(bits), 2), ",".join(sorted(wrong))
