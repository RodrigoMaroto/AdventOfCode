# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/9

from ...base import TextSolution, answer


def compute_checksum(file_blocks: list[tuple[int, int]], disk: list) -> int:
    file_positions = (
        idx
        for start, length in reversed(file_blocks)
        for idx in range(start + length - 1, start - 1, -1)
    )
    idx_file = next(file_positions)
    idx_disk = 0
    checksum = 0
    while idx_disk <= idx_file:
        if disk[idx_disk] == ".":
            checksum += idx_disk * disk[idx_file]
            idx_file = next(file_positions)
        else:
            checksum += idx_disk * disk[idx_disk]
        idx_disk += 1
    return checksum


def compute_checksum2(
    file_blocks: list[tuple[int, int]], disk: list, free_blocks: list[tuple[int, int]]
) -> int:
    checksum = 0
    for file_start, file_len in reversed(file_blocks):
        start = file_start
        for free_start, free_len in free_blocks:
            if free_start > file_start:
                break
            if free_len >= file_len:
                start = free_start
                idx = free_blocks.index((free_start, free_len))
                if file_len < free_len:
                    free_blocks[idx] = (free_start + file_len, free_len - file_len)
                else:
                    free_blocks.pop(idx)
                break
        checksum += sum(disk[file_start] * i for i in range(start, start + file_len))
    return checksum


class Solution(TextSolution):
    _year = 2024
    _day = 9

    @answer(6262891638328)
    def part_1(self) -> int:
        file_id = 0
        file_blocks, disk = [], []
        raw = [int(x) for x in self.input]
        for idx, block_len in enumerate(raw):
            if idx % 2 == 0:
                file_blocks.append((len(disk), block_len))
                disk += [file_id] * block_len
                file_id += 1
        return compute_checksum(file_blocks, disk)

    @answer((6262891638328, 6287317016845))
    def solve(self) -> tuple[int, int]:
        file_id = 0
        file_blocks, free_blocks, disk = [], [], []
        raw = [int(x) for x in self.input]
        for idx, block_len in enumerate(raw):
            if idx % 2 == 0:
                file_blocks.append((len(disk), block_len))
                disk += [file_id] * block_len
                file_id += 1
            else:
                free_blocks.append((len(disk), block_len))
                disk += ["."] * block_len
        return compute_checksum(file_blocks, disk), compute_checksum2(
            file_blocks, disk, free_blocks
        )
