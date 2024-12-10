# Day 9 (2024)

`Disk Fragmenter` ([prompt](https://adventofcode.com/2024/day/9))

Easy problem to brute force, but optimized it massively by reducing time complexity.

## Part 1
The input today consists on a list of digits that represent the partitions of a disk. The even positions represent the length of a file and alternatively, the odd positions are the length of empty blocks between the files. Additionally, each file has a `file ID` assigned secuencially. To illustrate it with an example:
```
12345 -> 0..111....22222
```
In order to handle it better, we will store this in two different structures. `disk` will be the same representation as you can see in the previous example. `file_blocks` will store for each file a tuple containg the index of the first block and the length.  

```py
def part_1(self) -> int:
    file_id = 0
    file_blocks, disk = [], []
    raw = [int(x) for x in self.input]
    for idx, block_len in enumerate(raw):
        if idx % 2 == 0:
            file_blocks.append((len(disk), block_len))
            disk += [file_id] * block_len
            file_id += 1
        else:
            disk += ["."] * block_len

```
In part 1, we need to reorder the memory blocks, moving the rightmost blocks to the leftmost empty positions, until there are free spaces between blocks. 

To do this I used the `compute_checksum` function. First of all, I use a generator to obtain the indexes of each memory block in reverse order. Then we loop the disk from both sides, filling empty blocks. Additionally, instead of changing the disk array, we can directly compute the required `checksum`, to do so we need to *add up the result of multiplying each of these blocks' position with the file ID number it contains*.

The function optimizes performance by using a generator to lazily generate file block positions and ensures efficient processing with a single pass through the disk.

```py
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
```

## Part 2
In this Part 2 we can only move complete files. To tackle this problem better, we can also track the `free_blocks` in the same format as `file_blocks`.
```py
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
```

For `compute_checksum2`, the logic will be slightly different as we need to take full blocks into account. We use a double loop to iterate through the files we need to move in reverse order and for each of those we scan the available empty blocks. After updating the `free_blocks`, we compute the checksum for that file and add it to the total.

```py
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

```

