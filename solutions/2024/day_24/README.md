# Day 24 (2024)

`Crossed Wires` ([prompt](https://adventofcode.com/2024/day/24))

Today’s challenge involves simulating a circuit of wires and logic gates to calculate binary values

## Part 1
The objective is to calculate the binary value of the "z" wires that would be the output of the system after propagating the circuit's logic. Each wire's value is determined by the values of its input wires and the logic gate connecting them.

To parse the input we need to consider the two parts it contains: initial wire values (`0` or `1` that will be encoded as a boolean) and logic gates.

to encode this input I used:
- A `wires` dictionary to store the boolean values of wires.
- An `operations` list to store all gate operations.
- The `highest_z` wire (highest-index "z" wire), which is used for the final binary output.
```py
class Solution(TextSolution):
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
```
I also created this helper function to compute the output of the logic gates that support three different operations: `AND`, `OR` and `XOR`.
```py
def process(op: str, op1: bool, op2: bool) -> bool:
    if op == "AND":
        return op1 & op2
    if op == "OR":
        return op1 | op2
    # "XOR"
    return op1 ^ op2
```
TO simulate the whole circuit the logic operations are evaluated iteratively:

1. For each operation, check if the input wires (`op1` and `op2`) have assigned values.
2. If both inputs are available, compute the result and assign it to the output wire (`res`).
3. Otherwise, append the operation back to the list for re-evaluation.

Finally, after all operations are processed, the "z" wires are sorted in descending order. Their values are concatenated into a binary string and converted to an integer, that is our required solution.
```py
class Solution(TextSolution):
    def part_1(self) -> int:
        ...

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
```

## Part 2

THe objective in this second part is to identify the invalid wires that prevent the system from correctly adding binary numbers, which is the system's expected behavior.


```py
class Solution(TextSolution):
    def part_2(self) -> str:
        ...

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
```
