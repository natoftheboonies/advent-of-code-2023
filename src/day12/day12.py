"""
Author: Nat with Darren's Template
Date: 2023-12-12

Solving https://adventofcode.com/2023/day/12

Part 1: recursively explore a sequence

Part 2: with 5x longer input

"""
import logging
import time
import aoc_common.aoc_commons as ac
from functools import cache

YEAR = 2023
DAY = 12

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


@cache
def explore(springs, sequence, pos=0, seq_id=0, seq_len=0):
    if pos == len(springs):
        # base cases, end of springs
        if seq_id == len(sequence) and seq_len == 0:
            # we have found all blocks and not currently in a block
            # logger.debug("happy ending")
            return 1
        elif seq_id == len(sequence) - 1 and seq_len == sequence[seq_id]:
            # current block is the last block
            # logger.debug("happy ending 2")
            return 1
        else:
            # no match
            # logger.debug("sad %s", (seq_id, seq_len))
            return 0
    else:
        # recursive cases
        valid_count = 0
        if springs[pos] == "?":
            # try .: end current sequence
            if seq_len == 0:
                # not currently in a block
                valid_count += explore(springs, sequence, pos + 1, seq_id, 0)
            elif seq_id < len(sequence) and sequence[seq_id] == seq_len:
                # end of current block
                valid_count += explore(springs, sequence, pos + 1, seq_id + 1, 0)
            # try #: extend current seq_id
            valid_count += explore(springs, sequence, pos + 1, seq_id, seq_len + 1)
        elif springs[pos] == ".":
            if seq_len == 0:
                # not currently in a block
                valid_count += explore(springs, sequence, pos + 1, seq_id, 0)
            elif seq_id < len(sequence) and sequence[seq_id] == seq_len:
                # end of current block
                valid_count += explore(springs, sequence, pos + 1, seq_id + 1, 0)
        elif springs[pos] == "#":
            # extend current seq_id
            valid_count += explore(springs, sequence, pos + 1, seq_id, seq_len + 1)
        else:
            logger.error("Unknown character %s", springs[pos])
        return valid_count


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)
    part1, part2 = 0, 0
    for line in data:
        left, right = line.strip().split()
        right = tuple([int(n) for n in right.split(",")])
        logger.debug("left: %s, right: %s", left, right)
        part1 += explore(left, right)
        # part 2, 5x longer
        left = "?".join(left for _ in range(5))
        right_extended = []
        for _ in range(5):
            right_extended.extend(right)
        # tuple for @cache
        right = tuple(right_extended)
        part2 += explore(left, right)

    logger.info("Part 1: %d", part1)
    logger.info("Part 2: %d", part2)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
