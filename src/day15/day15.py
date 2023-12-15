"""
Author: Nat with Darren's Template
Date: 2023-12-15

Solving https://adventofcode.com/2023/day/15

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 15

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def hash(data):
    current = 0
    for v in data:
        current += ord(v)
        current *= 17
        current %= 256
    return current


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    data = data[0].split(",")
    total = 0
    for i in data:
        total += hash(i)
    logger.info("Part 1: %d", total)


if __name__ == "__main__":
    t1 = time.perf_counter()
    hash("HASH")
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
